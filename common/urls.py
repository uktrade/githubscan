# -*- coding: utf-8 -*-
from django.urls import path

from .views import (
    handle_dispatch_email_reports,
    handle_dispatch_gecko_reports,
    handle_dispatch_slack_report,
    handle_refresh_vulnerability_data,
)

urlpatterns = [
    path(
        "refresh_vulnerability_data/",
        handle_refresh_vulnerability_data,
        name="refresh_vulnerability_data",
    ),
    path(
        "dispatch_gecko_reports/",
        handle_dispatch_gecko_reports,
        name="dispatch_gecko_reports",
    ),
    path(
        "dispatch_email_reports/",
        handle_dispatch_email_reports,
        name="dispatch_email_reports",
    ),
    path(
        "dispatch_slack_report/",
        handle_dispatch_slack_report,
        name="dispatch_slack_report",
    ),
]
