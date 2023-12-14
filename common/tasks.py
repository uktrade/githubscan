# -*- coding: utf-8 -*-
from celery import shared_task

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


@shared_task
def generate_scan_data():
    """refresh vulnerability data"""
    refresh_scan()
    refresh_processed_data()
    refresh_database()


@shared_task
def dispatch_email_reports():
    """dispatch emails"""
    dispatch_organization_email()
    dispatch_team_email()
    dispatch_team_detailed_email()


@shared_task
def dispatch_gecko_reports():
    """dispatch gecko board report"""
    dispatch_organization_gecko_report()
    dispatch_teams_gecko_report()


@shared_task
def dispatch_slack_report():
    """dispatch slack report"""
    dispatch_slack()
