# -*- coding: utf-8 -*-
from pathlib import Path
from typing import Any

from django.core.management.base import BaseCommand

from scanner.operators import refresh_scan


class Command(BaseCommand):
    help = refresh_scan.__doc__
    command_name = Path(__file__).stem

    def handle(self, *args: Any, **options: Any):
        refresh_scan()
