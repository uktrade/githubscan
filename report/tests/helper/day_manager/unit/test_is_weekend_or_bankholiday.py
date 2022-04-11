# -*- coding: utf-8 -*-
from datetime import date


def test_is_weekend_when_it_is_not(day_manager):
    Wednesday = date(2022, 4, 6)
    assert day_manager.is_weekend_or_bank_holiday(day=Wednesday) == False


def test_is_weekend_when_it_is(day_manager):
    Saturday = date(2022, 4, 9)
    assert day_manager.is_weekend_or_bank_holiday(day=Saturday) == True


def test_is_uk_bankholiday_when_it_weekday(day_manager):
    Wednesday = date(2022, 4, 6)
    assert day_manager.is_weekend_or_bank_holiday(day=Wednesday) == False


def test_is_uk_bankholiday_when_it_bankholiday(day_manager):
    Friday = date(2022, 4, 15)
    assert day_manager.is_weekend_or_bank_holiday(day=Friday) == True
