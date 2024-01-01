# -*- coding: utf-8 -*-
from pathlib import Path

import pytest

from common.functions import read_from_json_store, write_to_json_store

data_file = Path.joinpath(Path(__file__).parent, "test_data.json")


def test_read_from_json_store_non_existing_field(db, caplog):
    """test non existing field"""
    data = {"key": "value"}
    field = "not_existing"

    with pytest.raises(KeyError, match=f"{field} does not exist in JsonStore"):
        read_from_json_store(field=field)

    assert f"{field} does not exist in JsonStore" in caplog.messages


def test_read_from_json_store_existing_field(db, caplog):
    """test non existing field"""
    field_data = {"key": "value"}
    field = "scanned_data"

    write_to_json_store(data=field_data, field=field)

    field_data_in_db = read_from_json_store(field=field)

    assert field_data == field_data_in_db
    assert f"added data to field {field}" in caplog.messages
