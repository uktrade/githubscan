# -*- coding: utf-8 -*-
from pathlib import Path

from django.core.management.base import BaseCommand

from report.operators import refresh_database, refresh_processed_data


class Command(BaseCommand):
    help = refresh_processed_data.__doc__

    command_name = Path(__file__).stem

    def handle(self, *args, **kwargs):
        refresh_processed_data()
        refresh_database()
