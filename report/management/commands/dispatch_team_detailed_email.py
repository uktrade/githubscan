# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from report.report import dispatch_team_detailed_email
from common.functions import command_runner
from pathlib import Path


class Command(BaseCommand):
    help = dispatch_team_detailed_email.__doc__

    command_name = Path(__file__).stem

    @command_runner(command_name)
    def handle(*args, **options):
        dispatch_team_detailed_email(*args, **options)
