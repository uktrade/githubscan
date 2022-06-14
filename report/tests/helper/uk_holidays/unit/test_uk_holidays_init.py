# -*- coding: utf-8 -*-
from report.helper.uk_holidays import UKHolidays
from pathlib import Path
from django.conf import settings

DATA_FILE = Path.joinpath(Path(__file__).parent, settings.UK_HOLIDAYS_FILE_NAME)
MAX_DATA_FILE_AGE = 10


def test_init_with_non_posix_data_file(caplog):
    try:
        UKHolidays(
            data_file="/my/file/path",
            max_data_file_age=MAX_DATA_FILE_AGE,
            verify_ssl=False,
        )
        assert False
    except TypeError:
        assert "data_file expected to be PosixPath type but is str" in caplog.messages
        assert True


def test_init_with_string_as_max_data_file_age(caplog):
    try:
        UKHolidays(data_file=DATA_FILE, max_data_file_age="10", verify_ssl=False)
        assert False
    except TypeError:
        assert "max_data_file_age expected to be int type but is str" in caplog.messages
        assert True


def test_init_with_non_bool_verify_ssl(caplog):
    try:
        UKHolidays(
            data_file=DATA_FILE,
            max_data_file_age=MAX_DATA_FILE_AGE,
            verify_ssl="True",
        )
        assert False
    except TypeError:
        assert "verify_ssl expected to be bool type but is str" in caplog.messages
        assert True


def test_init_with_false_verify_ssl():
    try:
        UKHolidays(
            data_file=DATA_FILE,
            max_data_file_age=MAX_DATA_FILE_AGE,
            verify_ssl=False,
        )
        assert True
    except:
        assert False


def test_init_with_all_valid_params():
    try:
        UKHolidays(
            data_file=DATA_FILE,
            max_data_file_age=MAX_DATA_FILE_AGE,
            verify_ssl=False,
        )
        assert True
    except:
        assert False
