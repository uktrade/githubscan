# -*- coding: utf-8 -*-
from datetime import date


def test_exception_business_days_is_not_int(day_manager, caplog):
    try:
        saturday = date(2022, 4, 2)
        day_manager.business_days_to_calendar_days(
            start_date=saturday, business_days="10"
        )
        assert False
    except TypeError:
        assert "business_days expected to be int type but is str" in caplog.messages
        assert True


def test_date_start_on_saturday(day_manager):
    """
    2nd april 2022 was saturday
    """

    saturday = date(2022, 4, 2)
    business_days = 5

    calendar_days = day_manager.business_days_to_calendar_days(
        start_date=saturday, business_days=business_days
    )

    assert calendar_days == 6


def test_date_start_on_sunday(day_manager):
    """
    3rd april 2022 was Sunday
    """

    sunday = date(2022, 4, 3)
    business_days = 5

    calendar_days = day_manager.business_days_to_calendar_days(
        start_date=sunday, business_days=business_days
    )

    assert calendar_days == 5


def test_date_start_on_saturday_with_bankholiday(day_manager):
    """
     - 9th April 2022 was Saturday
     - 15th and 18th April were Bankholidays,
    so it shoudld count days until 19th April
    maning 5 working days == 10 calendar days
    """

    saturday = date(2022, 4, 9)
    business_days = 5
    calendar_days = day_manager.business_days_to_calendar_days(
        start_date=saturday, business_days=business_days
    )

    assert calendar_days == 10
