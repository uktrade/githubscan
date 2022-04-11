# -*- coding: utf-8 -*-
from datetime import date


def test_exception_calendar_days_is_not_int(day_manager, caplog):
    try:
        saturday = date(2022, 4, 2)
        day_manager.end_date(start_date=saturday, calendar_days="10")
        assert False
    except TypeError:
        assert "calendar_days expected to be int type but is str" in caplog.messages
        assert True


def test_date_start_on_saturday(day_manager):
    """
    2nd april 2022 was saturday
    """
    saturday = date(2022, 4, 2)
    calendar_days = 6
    end_date = day_manager.end_date(start_date=saturday, calendar_days=calendar_days)

    assert end_date == date(2022, 4, 8)


def test_date_start_on_sunday(day_manager):
    """
    3rd april 2022 was Sunday
    """
    sunday = date(2022, 4, 3)
    calendar_days = 5
    end_date = day_manager.end_date(start_date=sunday, calendar_days=calendar_days)

    assert end_date == date(2022, 4, 8)


def test_date_start_on_saturday_with_bankholiday(day_manager):
    """
     - 9th April 2022 was Saturday
     - 15th and 18th April were Bankholidays,
    so it shoudld count days until 19th April
    maning 5 working days == 10 calendar days
    """
    saturday = date(2022, 4, 9)
    calendar_days = 10
    end_date = day_manager.end_date(start_date=saturday, calendar_days=calendar_days)

    assert end_date == date(2022, 4, 19)
