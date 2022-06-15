# -*- coding: utf-8 -*-
from .views import (
    handle_refresh_vulneranility_data,
    handle_dispatch_gecko_reports,
    handle_dispatch_email_reports,
    handle_dispatch_slack_report,
)
from django.urls import path

urlpatterns = [
    path(
        "refresh_vulneranility_data/",
        handle_refresh_vulneranility_data,
        name="refresh_vulneranility_data",
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
