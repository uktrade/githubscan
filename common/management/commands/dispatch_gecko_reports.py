# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from report.operators import (
    dispatch_organization_gecko_report,
    dispatch_teams_gecko_report,
)


class Command(BaseCommand):
    help = "Dispatch gecko report"

    def handle(self, *args, **kwargs):
        dispatch_organization_gecko_report()
        dispatch_teams_gecko_report()
