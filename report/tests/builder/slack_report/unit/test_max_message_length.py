# -*- coding: utf-8 -*-
from django.conf import settings


def test_default_max_message_length(build_slack_report):

    assert build_slack_report.max_message_length == settings.SLACK_MESSAGE_LENGTH
    build_slack_report.clear()


def test_exception_max_message_length(build_slack_report, caplog):

    try:
        build_slack_report.max_message_length = "30"
        assert False
    except TypeError:
        assert "length expected to be int type but is str" in caplog.messages
        assert True


def test_setting_max_message_length(build_slack_report):

    build_slack_report.max_message_length = 30
    assert build_slack_report.max_message_length == 30
