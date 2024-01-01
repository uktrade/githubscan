# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand

from report.operators import dispatch_team_detailed_email


class Command(BaseCommand):
    help = dispatch_team_detailed_email.__doc__

    command_name = Path(__file__).stem

    def handle(self, *args: Any, **options: Any):
        dispatch_team_detailed_email()
