# -*- coding: utf-8 -*-
from report.db import remove_duplicate_team_notification_targets
from django.core.management.base import BaseCommand
from common.functions import command_runner
from pathlib import Path


class Command(BaseCommand):
    help = remove_duplicate_team_notification_targets.__doc__

    command_name = Path(__file__).stem

    @command_runner(command_name)
    def handle():
        remove_duplicate_team_notification_targets()
