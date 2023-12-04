# -*- coding: utf-8 -*-
from pathlib import Path

from common.functions import delete_file_if_exist, write_json_file

data_file = Path.joinpath(Path(__file__).parent, "test_delete.json")


def test_delete_existing_file(caplog):
    data = {"key": "value"}
    write_json_file(data=data, dest_file=data_file)

    try:
        delete_file_if_exist(dest_file=data_file)
        assert True
    except:
        assert False

    assert f"removed: {data_file}" in caplog.messages


def test_delete_non_existing_file(caplog):
    try:
        delete_file_if_exist(dest_file=data_file)
        assert False
    except:
        assert True

    assert f"{data_file} file does not exist" in caplog.messages
