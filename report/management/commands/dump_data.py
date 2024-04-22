# -*- coding: utf-8 -*-
import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from common.functions import read_from_json_store


class Command(BaseCommand):

    command_name = Path(__file__).stem

    def handle(self, *args, **kwargs):
        scanned_data = read_from_json_store(field=settings.SCANNER_DATA_FIELD_NAME)

        with open("scanner_data.json", "w") as file:
            file.write(json.dumps(scanned_data, indent=4, sort_keys=True))

        processed_data = read_from_json_store(field=settings.PROCESSED_DATA_FIELD)

        with open("processed_data.json", "w") as file:
            file.write(json.dumps(processed_data, indent=4, sort_keys=True))
