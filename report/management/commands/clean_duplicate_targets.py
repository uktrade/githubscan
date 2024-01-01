# -*- coding: utf-8 -*-
from pathlib import Path

from django.core.management.base import BaseCommand

from report.db import remove_duplicate_team_notification_targets


class Command(BaseCommand):
    help = remove_duplicate_team_notification_targets.__doc__

    command_name = Path(__file__).stem

    def handle(self, *args, **kwargs):
        remove_duplicate_team_notification_targets()
