# -*- coding: utf-8 -*-
from datetime import date


def test_exception_business_days_start_date_is_greater_than_end_date(day_manager):
    try:
        start_date = date(2022, 4, 11)
        end_date = date(2022, 4, 4)
        day_manager.business_days_between(start_date=start_date, end_date=end_date)
        assert False
    except ValueError:
        assert True


def test_business_days_between_Monday_to_Sunday(day_manager):
    start_date = date(2022, 4, 4)
    end_date = date(2022, 4, 10)

    assert 4 == day_manager.business_days_between(
        start_date=start_date, end_date=end_date
    )


def test_business_days_between_Monday_to_Saturday(day_manager):
    start_date = date(2022, 4, 4)
    end_date = date(2022, 4, 9)

    assert 4 == day_manager.business_days_between(
        start_date=start_date, end_date=end_date
    )


def test_business_days_between_Monday_to_Friday(day_manager):
    start_date = date(2022, 4, 4)
    end_date = date(2022, 4, 8)

    assert 4 == day_manager.business_days_between(
        start_date=start_date, end_date=end_date
    )


def test_business_days_with_bankholidys(day_manager):
    """
    11th April 2022 was Monday and a working day, however following
        - friday (15th April 2022)
        - Monday (18th April 2022)
    so, starting from 11th April to 19th April Tuesday ( which is excluded in count)
    we will have 4 business days
    """
    start_date = date(2022, 4, 11)
    end_date = date(2022, 4, 19)

    assert 4 == day_manager.business_days_between(
        start_date=start_date, end_date=end_date
    )
