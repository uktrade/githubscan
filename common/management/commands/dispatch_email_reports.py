# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand

from report.operators import (
    dispatch_organization_email,
    dispatch_team_detailed_email,
    dispatch_team_email,
)


class Command(BaseCommand):
    help = "Dispatach all report emails"

    def handle(self, *args, **kwargs):
        dispatch_organization_email()
        dispatch_team_email()
        dispatch_team_detailed_email()
