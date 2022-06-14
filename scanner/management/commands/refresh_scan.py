# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
from scanner import refresh_scan
from common.functions import command_runner
from pathlib import Path


class Command(BaseCommand):
    help = refresh_scan.__doc__

    command_name = Path(__file__).stem

    @command_runner(command_name)
    def handle(self, *args, **options):
        refresh_scan(*args, **options)
