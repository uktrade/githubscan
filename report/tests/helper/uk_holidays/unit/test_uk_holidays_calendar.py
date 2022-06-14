# -*- coding: utf-8 -*-
from django.conf import settings


def test_exception_in_calendar(uk_holidays):
    try:
        uk_holidays.calendar_url = "https://httpbin.org/get"
        assert False
    except KeyError:
        assert True


def test_empty_calender_before_setter_is_called(uk_holidays):
    assert uk_holidays.calendar == []
    assert len(uk_holidays.calendar) == 0
    uk_holidays.clear()


def test_exception_in_calendar(uk_holidays):
    try:
        uk_holidays.calendar_url = settings.UK_HOLIDAYS_SOURCE_URL
        assert len(uk_holidays.calendar) >= 1
        assert True
        uk_holidays.clear()
        uk_holidays.uk_holidays_file.unlink()
    except:
        assert False
