# -*- coding: utf-8 -*-
from datetime import date


def test_working_days_between_dates_start_date_is_weekend(day_manager):
    """
    9th April 2022 was Saturday
    """
    end_date = date(2022, 4, 14)
    start_date = date(2022, 4, 9)

    working_days = day_manager.working_days_between_dates(
        end_date=end_date, start_date=start_date
    )

    assert working_days == 4


def test_working_days_between_dates_start_date_is_working_day(day_manager):
    """
    11th April 2022 was Monday
    """
    end_date = date(2022, 4, 14)
    start_date = date(2022, 4, 11)

    working_days = day_manager.working_days_between_dates(
        end_date=end_date, start_date=start_date
    )

    assert working_days == 3


def test_working_days_between_dates_start_date_is_long_weekend(day_manager):
    """
    15th April 2022 was Friday and long weekend
    """
    end_date = date(2022, 4, 20)
    start_date = date(2022, 4, 15)

    working_days = day_manager.working_days_between_dates(
        end_date=end_date, start_date=start_date
    )

    assert working_days == 2


def test_working_days_between_dates_start_date_is_after_end_date(day_manager):
    """
    both are working days
    """
    end_date = date(2022, 4, 7)
    start_date = date(2022, 4, 11)

    working_days = day_manager.working_days_between_dates(
        end_date=end_date, start_date=start_date
    )

    assert working_days == -2


def test_working_days_between_dates_start_date_afte_end_date_and_is_weekend(
    day_manager,
):
    """
    Start date is sunday
    """
    end_date = date(2022, 4, 7)
    start_date = date(2022, 4, 10)

    working_days = day_manager.working_days_between_dates(
        end_date=end_date, start_date=start_date
    )

    assert working_days == -1


def test_working_days_between_dates_start_date_afte_end_date_and_is_long_weekend(
    day_manager,
):
    """
    Start date is sunday
    """
    end_date = date(2022, 4, 11)
    start_date = date(2022, 4, 18)

    working_days = day_manager.working_days_between_dates(
        end_date=end_date, start_date=start_date
    )

    assert working_days == -3
