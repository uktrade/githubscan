# -*- coding: utf-8 -*-
from pathlib import Path

from django.core.management.base import BaseCommand

from report.operators import dispatch_organization_email


class Command(BaseCommand):
    help = dispatch_organization_email.__doc__

    command_name = Path(__file__).stem

    def handle(self, *args, **kwargs):
        dispatch_organization_email()
