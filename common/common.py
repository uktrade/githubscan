# -*- coding: utf-8 -*-
from scanner.scanner import refresh_scan
from report.report import refresh_processed_data, refresh_database
from report.report import (
    dispatch_organization_email,
    dispatch_team_email,
    dispatch_team_detailed_email,
)
from report.report import (
    dispatch_organization_gecko_report,
    dispatch_teams_gecko_report,
)
from report.report import dispatch_slack


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
