# -*- coding: utf-8 -*-
from common.functions import load_json_file
import json
from pathlib import Path

data_file = Path.joinpath(Path(__file__).parent, "test_data.json")


def test_load_json_data_file_does_not_exist(caplog):

    try:
        load_json_file(src_file=data_file)
        assert False
    except FileNotFoundError:
        assert True

    assert f"[Errno 2] No such file or directory: '{data_file}'" in caplog.messages


def test_load_json_data_file_with_empty_data(caplog):

    with open(data_file, "w") as file:
        content = json.dumps({})
        file.write(content)

    try:
        data = load_json_file(src_file=data_file)

        assert data == {}

        if data_file.exists():
            data_file.unlink()

        assert True

    except:
        assert False


def test_load_json_data_file_with_data(caplog):

    data = {"key": "value"}
    with open(data_file, "w") as file:
        content = json.dumps(data)
        file.write(content)

    try:
        loaded_data = load_json_file(src_file=data_file)

        assert data == loaded_data

        if data_file.exists():
            data_file.unlink()

        assert True

    except:
        assert False
