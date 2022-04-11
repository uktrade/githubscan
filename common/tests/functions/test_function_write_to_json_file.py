# -*- coding: utf-8 -*-
from common.functions import write_json_file
from pathlib import Path

data_file = Path.joinpath(Path(__file__).parent, "test_data.json")


def test_write_to_json_file_incorrect_data_type(caplog):
    data = "text"

    try:
        write_json_file(data=data, dest_file=data_file)
        assert False
    except TypeError:
        assert True

    assert f"data expected to be dict type but is str" in caplog.messages


def test_write_to_json_file_inccorrect_dest_file_type(caplog):
    data = {"key": "value"}

    try:
        write_json_file(data=data, dest_file=dict(data_file))
        assert False
    except TypeError:
        assert True


def test_write_to_json_correct_data_and_posix_dest_file(caplog):
    data = {"key": "value"}

    try:
        write_json_file(data=data, dest_file=data_file)
        assert True
    except:
        assert False

    assert f"created {data_file}" in caplog.messages

    assert data_file.exists()

    if data_file.exists():
        data_file.unlink()


def test_write_to_json_correct_data_and_string_dest_file(caplog):
    data = {"key": "value"}

    try:
        write_json_file(data=data, dest_file=str(data_file))
        assert True
    except:
        assert False

    assert f"created {data_file}" in caplog.messages

    assert data_file.exists()

    if data_file.exists():
        data_file.unlink()
