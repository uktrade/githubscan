# -*- coding: utf-8 -*-
from django.conf import settings
from django.http import HttpResponse
from requests import request

from common.common import (
    dispatch_email_reports,
    dispatch_gecko_reports,
    dispatch_slack_report,
    refresh_vulnerability_data,
)
from common.functions import job_runner

"""
this method provides a way to refresh report data
Reason: Since, now reports are in file, it has been observered that
executing command directly in PaaS as a task results in files to get written in task container
with view we will attempt to write files on container
"""


def _check_host_(request):
    expected_host_name = settings.ALLOWED_REPORT_ENDPOINT_HOSTS
    actual_host_name = request.get_host().split(":")[0]

    if actual_host_name in expected_host_name:
        return True

    return False


def handle_refresh_vulnerability_data(request):
    if _check_host_(request=request):
        job_runner("refresh_vulnerability_data", refresh_vulnerability_data)

    return HttpResponse("Done")


def handle_dispatch_email_reports(request):
    if _check_host_(request=request):
        job_runner("dispatch_email_reports", dispatch_email_reports)

    return HttpResponse("Done")


def handle_dispatch_gecko_reports(request):
    if _check_host_(request=request):
        job_runner("dispatch_gecko_reports", dispatch_gecko_reports)

    return HttpResponse("Done")


def handle_dispatch_slack_report(request):
    if _check_host_(request=request):
        job_runner("dispatch_slack_report", dispatch_slack_report)

    return HttpResponse("Done")
