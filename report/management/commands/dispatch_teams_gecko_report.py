# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand

from report.operators import dispatch_teams_gecko_report


class Command(BaseCommand):
    help = dispatch_teams_gecko_report.__doc__

    command_name = Path(__file__).stem

    def handle(self, *args: Any, **options: Any):
        dispatch_teams_gecko_report()
