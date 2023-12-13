# -*- coding: utf-8 -*-
from report.report import (
    dispatch_organization_email,
    dispatch_organization_gecko_report,
    dispatch_slack,
    dispatch_team_detailed_email,
    dispatch_team_email,
    dispatch_teams_gecko_report,
    refresh_database,
    refresh_processed_data,
)
from scanner.scanner import refresh_scan


def refresh_vulnerability_data():
    refresh_scan()
    refresh_processed_data()
    refresh_database()


def dispatch_email_reports():
    dispatch_organization_email()
    dispatch_team_email()
    dispatch_team_detailed_email()


def dispatch_gecko_reports():
    dispatch_organization_gecko_report()
    dispatch_teams_gecko_report()


def dispatch_slack_report():
    dispatch_slack()
