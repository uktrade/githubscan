# -*- coding: utf-8 -*-
from django.conf import settings


def test_max_report_repositories_default(build_gecko_report):

    assert (
        build_gecko_report.max_report_repositories
        == settings.GECKO_BOARD_TOP_N_REPOSITORIES
    )


def test_exception_max_report_repositories_setter(build_gecko_report, caplog):
    try:
        build_gecko_report.max_report_repositories = "20"
        assert False
    except TypeError:
        assert "max_count expected to be int type but is str" in caplog.messages
        assert True


def test_max_report_repositories_valid_value(build_gecko_report):
    build_gecko_report.max_report_repositories = 2

    assert build_gecko_report.max_report_repositories == 2

    build_gecko_report.clear()
