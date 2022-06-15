# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from common.common import dispatch_email_reports
from common.functions import command_runner
from pathlib import Path


class Command(BaseCommand):
    help = "Dispatach all report emails"

    command_name = Path(__file__).stem

    @command_runner(command_name)
    def handle():
        dispatch_email_reports()
