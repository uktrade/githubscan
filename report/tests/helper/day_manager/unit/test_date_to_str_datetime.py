# -*- coding: utf-8 -*-
from datetime import datetime, date


def test_exception_date_a_string(day_manager):
    try:
        day = "2022-04-09T00:00:00Z"
        day_manager.date_to_str_datetime(date=day)
        assert False
    except TypeError:
        assert True


def test_date_is_date_obj(day_manager):
    day = "2022-04-09T00:00:00Z"
    day_obj = date(2022, 4, 9)

    assert day == day_manager.date_to_str_datetime(date=day_obj)


def test_date_is_datetime_obj(day_manager):
    day = "2022-04-09T08:42:30Z"
    day_obj = datetime(2022, 4, 9, 8, 42, 30)

    assert day == day_manager.date_to_str_datetime(date=day_obj)
