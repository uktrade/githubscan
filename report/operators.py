# -*- coding: utf-8 -*-
import json
import logging

from django.conf import settings

from common.functions import read_from_json_store, write_to_json_store
from config.schema import processed_data_schema
from config.severities import SEVERITY_STATUS
from report.builder.csv_report import BuildCSVReport

# Email Dispatch
from report.builder.email_report import BuildEmailReport

# Gecko Dispatch
from report.builder.gecko_report import BuildGeckoReport

# Slack Dispatch
from report.builder.slack_report import BuildSlackReport
from report.db import (
    get_reportable_organization_notification_targets,
    get_reportable_teams_from_db,
    get_team_notification_targets,
    remove_duplicate_team_notification_targets,
    update_enterprise_users_in_db,
    update_sso_notification_targets_in_db,
    update_teams_in_db,
)
from report.dispatchers import SlackClient
from report.dispatchers.email_client import EmailClient
from report.dispatchers.gecko_client import GeckoClient
from report.processor import ReportDataProcessor
from report.reader import ReportReader

report_reader = ReportReader()
logger = logging.getLogger(__name__)


def create_processed_data(scanner_data):
    """
    This function builds the report data, which will than be used to dispatch reports

    Parameters:
    -----------
    scanner_data: input data file , meaning we need to run refresh scan before we run report generation
    processed_data: this is output file, where we will dump the content of report
    """

    processor = ReportDataProcessor()
    processor.load_data_from_dict = scanner_data
    processor.add_enterprise_users()
    processor.add_sso_notification_targets()
    processor.add_repositories()
    processor.add_repository_teams()
    processor.add_vulnerable_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_fix_by_date()
    processor.add_hash()
    processor.add_repository_severity_status()
    processor.add_repository_totals()
    processor.add_skip_scan_repositories()
    processor.add_skip_scan_repositories_severity_status()
    processor.add_skip_scan_repositories_totals()
    processor.add_teams_and_team_repositories()
    processor.enforce_exclusive_team_repositories()
    processor.add_team_severity_status()
    processor.add_team_totals()
    processor.add_token_has_no_access()
    processor.add_organization_severity_status()
    processor.add_organization_totals()
    processor.add_orphan_repositories()
    processor.add_orphan_repositories_severity_status()
    processor.add_orphan_repositories_totals()
    processed_data_schema.validate(processor.processed_data)
    return processor.processed_data


def write_processed_data(
    processed_data, processed_data_field=settings.PROCESSED_DATA_FIELD
):
    """write processed data to json field"""
    write_to_json_store(data=processed_data, field=processed_data_field)


def refresh_database():
    """
    This function simply updates data base with
     - enterprise users and
     - teams
    which is used for the dispatching email eventually
    Note: Not tested , needs integration testing
    """

    global report_reader
    report_reader.load_processed_data = settings.PROCESSED_DATA_FIELD

    github_teams = list(report_reader.teams.keys())

    update_teams_in_db(github_teams=github_teams)

    update_enterprise_users_in_db(enterprise_users=report_reader.enterprise_users)

    update_sso_notification_targets_in_db(
        sso_notification_targets=report_reader.sso_notification_targets
    )

    remove_duplicate_team_notification_targets()

    report_reader.clear()


def refresh_processed_data():
    """
    Loads scanned data from file , process it and write to process data file
    which will than be used for building reports

    Note: Not tested , needs integration testing
    """
    scanner_data = read_from_json_store(field=settings.SCANNER_DATA_FIELD_NAME)
    processed_data = create_processed_data(scanner_data=scanner_data)

    write_processed_data(
        processed_data=processed_data,
        processed_data_field=settings.PROCESSED_DATA_FIELD,
    )
    processed_data.clear()


def dispatch_slack():
    """
    This function dispatches report to slack channel
    """
    global report_reader

    report_reader.load_processed_data = settings.PROCESSED_DATA_FIELD
    if settings.ENABLE_SLACK_NOTIFY:
        slack_report = BuildSlackReport()
        slack_report.organization(report_reader=report_reader)
        slack_report.organization_slo_breach(report_reader=report_reader)
        slack_report.teams(report_reader=report_reader)
        slack_report.orphan_repositories(report_reader=report_reader)
        slack_report.orphan_repositories_list(report_reader=report_reader)
        slack_report.unmonitored_repositories(report_reader=report_reader)
        slack_report.unmonitored_repositories_list(report_reader=report_reader)

        report_data = json.dumps(
            {"channel": settings.SLACK_CHANNEL, "blocks": slack_report.slack_message}
        )

        slack_client = SlackClient()
        slack_client.url = settings.SLACK_URL
        slack_client.auth_header = slack_client.bearer_auth_header
        slack_client.auth_token = settings.SLACK_AUTH_TOKEN

        slack_client.post_query = report_data

        slack_report.clear()
        slack_client.clear()
        report_data = ""

        report_reader.clear()
    else:
        logger.info("set ENABLE_SLACK_NOTIFY to true to use slack notification")


def dispatch_organization_email():
    """
    This function dispatches summary email
    """
    report_reader.load_processed_data = settings.PROCESSED_DATA_FIELD

    build_email_report = BuildEmailReport()
    build_csv_report = BuildCSVReport()

    report_data = build_email_report.organization_summary(report_reader=report_reader)

    report_file = build_csv_report.organization_report(report_reader=report_reader)

    email_client = EmailClient()
    for receiver in get_reportable_organization_notification_targets():
        email_client.send_email_with_attachment(
            receiver_email=receiver.email,
            upload_file_path=report_file,
            data=report_data,
            notify_template_id=settings.GOV_NOTIFY_SUMMARY_REPORT_TEMPLATE_ID,
        )

    report_reader.clear()
    build_email_report.clear()
    build_csv_report.clear()
    report_file.unlink()


def dispatch_team_email():
    """
    This function sends detailed email to each team
    """
    global report_reader

    report_reader.load_processed_data = settings.PROCESSED_DATA_FIELD

    build_email_report = BuildEmailReport()
    build_csv_report = BuildCSVReport()

    email_client = EmailClient()

    for team in set(get_reportable_teams_from_db()):
        team_notification_targets = get_team_notification_targets(team=team)
        report_data = build_email_report.teams_summary(
            team=team.name, report_reader=report_reader
        )

        report_file = build_csv_report.team_report(
            team=team.name, report_reader=report_reader
        )

        for email_info in team_notification_targets:
            if email_info.red_alerts_only:
                if SEVERITY_STATUS.RED.name != report_data["severity_status"]:
                    continue

            # do not send green alert
            if email_info.no_green_alerts:
                if SEVERITY_STATUS.GREEN.name == report_data["severity_status"]:
                    continue

            email_client.send_email_with_attachment(
                receiver_email=email_info.email,
                upload_file_path=report_file,
                data=report_data,
                notify_template_id=settings.GOV_NOTIFY_SUMMARY_REPORT_TEMPLATE_ID,
            )

        build_email_report.clear()
        report_data.clear()
        report_file.unlink()

    report_reader.clear()


def dispatch_team_detailed_email():
    """
    This function dispatches detailed emails to team
    """
    global report_reader

    report_reader.load_processed_data = settings.PROCESSED_DATA_FIELD

    build_email_report = BuildEmailReport()

    email_client = EmailClient()

    for team in set(get_reportable_teams_from_db()):
        team_notification_targets = get_team_notification_targets(team=team)
        report_data = build_email_report.team_detailed(
            team=team.name, report_reader=report_reader
        )

        """
        We send detailed emails only if there is something to send
        """
        if report_data and report_data["content"]:
            for email_info in team_notification_targets:
                if email_info.red_alerts_only:
                    if SEVERITY_STATUS.RED.name != report_data["severity_status"]:
                        continue

                email_client.send_email(
                    receiver_email=email_info.email,
                    data=report_data,
                    notify_template_id=settings.GOV_NOTIFY_DETAILED_REPORT_TEMPLATE_ID,
                )

        build_email_report.clear()
        report_data.clear()

    report_reader.clear()


def dispatch_organization_gecko_report():
    """
    This function dispatches organization report to gecko board
    """
    global report_reader

    report_reader.load_processed_data = settings.PROCESSED_DATA_FIELD

    build_gecko_report = BuildGeckoReport()

    gb_client = GeckoClient()

    build_gecko_report.organizaition(report_reader=report_reader)

    gb_client.send_organization_report(
        organization_data=build_gecko_report.organization_report
    )

    report_reader.clear()
    build_gecko_report.clear()


def dispatch_teams_gecko_report():
    """
    This function dispatches organization report to gecko board
    """
    global report_reader

    report_reader.load_processed_data = settings.PROCESSED_DATA_FIELD

    build_gecko_report = BuildGeckoReport()

    gb_client = GeckoClient()

    build_gecko_report.teams(report_reader=report_reader)

    for team, team_data in build_gecko_report.teams_report.items():
        gb_client.send_team_report(team=team, team_data=team_data)

    report_reader.clear()
    build_gecko_report.clear()
