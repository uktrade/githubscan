# -*- coding: utf-8 -*-
"""
note testing the max char length, since django does not apply any limit on this field
https://docs.djangoproject.com/en/4.2/ref/models/fields/#textfield
"""
import json
from pathlib import Path

import pytest

from common.functions import write_to_json_store
from common.models import JsonStore

data_file = Path.joinpath(Path(__file__).parent, "test_data.json")


def test_write_to_json_store_incorrect_data_type(caplog):
    """test invalid data type"""
    data = "text"

    try:
        write_to_json_store(data=data, field="does_not_matter")
        assert False
    except TypeError:
        assert True

    assert "data expected to be dict type but is str" in caplog.messages


def test_write_to_json_store_non_existing_field(db, caplog):
    """test non existing field"""
    data = {"key": "value"}
    field = "not_existing"

    with pytest.raises(KeyError, match=f"{field} does not exist in JsonStore"):
        write_to_json_store(data=data, field=field)

    assert f"{field} does not exist in JsonStore" in caplog.messages


def test_write_to_json_store_existing_field(db, caplog):
    """test non existing field"""
    field_data = {"key": "value"}
    field = "scanned_data"

    write_to_json_store(data=field_data, field=field)

    field_data_in_db = json.loads(JsonStore.objects.values()[0][field])

    assert field_data == field_data_in_db
    assert f"added data to field {field}" in caplog.messages
