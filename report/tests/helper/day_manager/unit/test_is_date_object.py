# -*- coding: utf-8 -*-
from datetime import datetime, date


def test_object_is_not_date(day_manager):
    try:
        Saturday = datetime(2022, 4, 9)
        day_manager._is_date(obj=Saturday)
        assert False
    except TypeError:
        assert True


def test_object_is_a_date(day_manager):
    try:
        Saturday = date(2022, 4, 9)
        assert day_manager._is_date(obj=Saturday) == True
        assert True
    except TypeError:
        assert False
