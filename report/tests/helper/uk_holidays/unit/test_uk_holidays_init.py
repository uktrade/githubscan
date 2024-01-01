# -*- coding: utf-8 -*-

from django.conf import settings

from report.helper.uk_holidays import UKHolidays


def test_init_with_non_bool_verify_ssl(caplog):
    try:
        UKHolidays(verify_ssl="True")
        assert False
    except TypeError:
        assert "verify_ssl expected to be bool type but is str" in caplog.messages
        assert True


def test_init_with_false_verify_ssl():
    try:
        UKHolidays(verify_ssl=False)
        assert True
    except:
        assert False


def test_init_with_default():
    try:
        UKHolidays()
        assert True
    except:
        assert False
