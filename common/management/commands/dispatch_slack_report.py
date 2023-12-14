# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from common.tasks import dispatch_slack_report


class Command(BaseCommand):
    help = "Dispatch slack reports"

    def handle(self, *args, **kwargs):
        dispatch_slack_report.delay()
