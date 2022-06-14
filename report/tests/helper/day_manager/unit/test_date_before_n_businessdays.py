# -*- coding: utf-8 -*-
from datetime import date


def test_exception_non_int_business_days(day_manager, caplog):
    try:
        end_date = date(2022, 4, 4)
        day_manager.date_before_n_business_days(end_date=end_date, business_days=10.3)
        assert False
    except TypeError:
        assert "business_days expected to be int type but is float" in caplog.messages
        assert True


def test_start_with_sunday_to_count_5_business_days_back(day_manager):
    start_date = date(2022, 4, 1)
    end_date = date(2022, 4, 10)

    assert start_date == day_manager.date_before_n_business_days(
        end_date=end_date, business_days=5
    )


def test_start_with_saturday_to_count_5_business_days_back(day_manager):
    start_date = date(2022, 4, 1)
    end_date = date(2022, 4, 9)

    assert start_date == day_manager.date_before_n_business_days(
        end_date=end_date, business_days=5
    )


def test_start_with_friday_to_count_4_business_days_back(day_manager):
    start_date = date(2022, 4, 4)
    end_date = date(2022, 4, 8)

    assert start_date == day_manager.date_before_n_business_days(
        end_date=end_date, business_days=4
    )


def test_start_with_bankholiday_to_count_4_business_days_back(day_manager):
    """
    11th April 2022 was Monday and a working day, however following
        - friday (15th April 2022)
        - Monday (18th April 2022)
    so, starting from 11th April to 19th April Tuesday ( which is excluded in count)
    we will have 4 business days
    """
    start_date = date(2022, 4, 11)
    end_date = date(2022, 4, 19)
    assert start_date == day_manager.date_before_n_business_days(
        end_date=end_date, business_days=4
    )
