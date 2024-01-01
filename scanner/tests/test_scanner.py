# -*- coding: utf-8 -*-

from django.conf import settings

from config.schema import scanner_data_schema
from scanner.operators import create_scanner_data, read_scanner_data, write_scanner_data


def test_scanner_data(real_test, db):
    data_field = settings.SCANNER_DATA_FIELD_NAME

    scanner_data = create_scanner_data()

    assert scanner_data_schema.is_valid(scanner_data)

    write_scanner_data(scanner_data=scanner_data, dest_field=data_field)

    scanner_data_from_db = read_scanner_data(
        dest_field=settings.SCANNER_DATA_FIELD_NAME
    )
    for key in scanner_data_from_db.keys():
        assert scanner_data[key] == scanner_data_from_db[key]
