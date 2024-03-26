# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from report.operators import dispatch_slack


class Command(BaseCommand):
    help = "Dispatch slack reports"

    def handle(self, *args, **kwargs):
        dispatch_slack()
