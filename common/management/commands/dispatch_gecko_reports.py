# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from common.tasks import dispatch_gecko_reports


class Command(BaseCommand):
    help = "Dispatch gecko report"

    def handle(self, *args, **kwargs):
        dispatch_gecko_reports.delay()
