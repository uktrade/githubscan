# -*- coding: utf-8 -*-
from datetime import datetime, date
from config.date_formats import DATE_FORMAT


def test_str_date_is_date_obj(day_manager):
    try:
        day = date(2022, 4, 9)
        day_manager._str_to_date(str_date=day, format=DATE_FORMAT.DATE.value)
        assert False
    except TypeError:
        assert True


def test_str_date_is_datetime(day_manager):
    try:
        day = datetime(2022, 4, 9)
        day_manager._str_to_date(str_date=day, format=DATE_FORMAT.DATE.value)
        assert False
    except TypeError:
        assert True


def test_str_date_is_invalid_formate(day_manager):
    try:
        day = "22-04-09"
        day_manager._str_to_date(str_date=day, format=DATE_FORMAT.DATE.value)
        assert False
    except ValueError:
        assert True


def test_str_date_is_outof_bound(day_manager):
    try:
        day = "22-04-33"
        day_manager._str_to_date(str_date=day, format=DATE_FORMAT.DATE.value)
        assert False
    except ValueError:
        assert True


def test_str_month_is_outof_bound(day_manager):
    try:
        day = "22-13-09"
        day_manager._str_to_date(str_date=day, format=DATE_FORMAT.DATE.value)
        assert False
    except ValueError:
        assert True


def test_str_date_not_matching_with_regex(day_manager):
    try:
        day = "22022-04-09T08:42:00Z"
        day_manager._str_to_date(str_date=day, format=DATE_FORMAT.DATE.value)
        assert False
    except ValueError:
        assert True


def test_str_date_to_date(day_manager):
    day = "2022-04-09"
    day_obj = date(2022, 4, 9)
    assert day_obj == day_manager._str_to_date(
        str_date=day, format=DATE_FORMAT.DATE.value
    )


def test_str_datetime_to_date(day_manager):
    day = "2022-04-09T08:42:00Z"
    day_obj = date(2022, 4, 9)
    assert day_obj == day_manager._str_to_date(
        str_date=day, format=DATE_FORMAT.DATE_TIME.value
    )
