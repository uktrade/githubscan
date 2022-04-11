# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from report.report import (
    dispatch_organization_gecko_report,
    dispatch_teams_gecko_report,
)
from common.functions import command_runner
from pathlib import Path


class Command(BaseCommand):
    help = "Dispatach all gecko reports"

    command_name = Path(__file__).stem

    @command_runner(command_name)
    def handle(*args, **options):
        dispatch_organization_gecko_report(*args, **options)
        dispatch_teams_gecko_report(*args, **options)
