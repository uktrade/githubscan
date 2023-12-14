# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from common.tasks import dispatch_email_reports


class Command(BaseCommand):
    help = "Dispatach all report emails"

    def handle(self, *args, **kwargs):
        dispatch_email_reports.delay()
