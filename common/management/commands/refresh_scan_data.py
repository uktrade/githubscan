# -*- coding: utf-8 -*-

from django.core.management.base import BaseCommand

from common.tasks import refresh_report_data, refresh_scan_data


class Command(BaseCommand):
    """Refresh Vulnerabilities Data"""

    help = "Refresh Vulnerabilities Data"

    def handle(self, *args, **kwargs):
        refresh_scan_data.delay()
