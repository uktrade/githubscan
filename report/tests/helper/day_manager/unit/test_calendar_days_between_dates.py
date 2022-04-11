# -*- coding: utf-8 -*-
from datetime import date


def test_exception_calendar_days_start_date_is_greater_than_end_date(day_manager):
    try:
        start_date = date(2022, 4, 11)
        end_date = date(2022, 4, 4)
        day_manager.calendar_days_between(start_date=start_date, end_date=end_date)
        assert False
    except ValueError:
        assert True


def test_calendar_days_between(day_manager):
    start_date = date(2022, 4, 4)
    end_date = date(2022, 4, 11)

    assert 7 == day_manager.calendar_days_between(
        start_date=start_date, end_date=end_date
    )
