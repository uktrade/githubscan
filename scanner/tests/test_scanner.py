# -*- coding: utf-8 -*-
from scanner import create_scanner_data, write_scanner_data
from django.conf import settings
from config.schema import scanner_data_schema
from pathlib import Path


def test_scanner_data(real_test):
    try:
        data_file = Path.joinpath(
            Path(__file__).parent, settings.SCANNER_DATA_FILE_NAME
        )

        assert data_file.exists() == False

        scanner_data = create_scanner_data()

        assert scanner_data_schema.is_valid(scanner_data)

        write_scanner_data(scanner_data=scanner_data, dest_file=data_file)

        assert data_file.exists() == True

        data_file.unlink()

        assert True
    except:
        assert False
