# -*- coding: utf-8 -*-
from common.functions import url_checker


def test_url_checker_with_non_string_url(caplog):
    try:
        url = {"this": "will never work"}
        url_checker(url=url)
        assert False
    except:
        assert True
        assert "url expected to be str type but is dict" in caplog.messages


def test_url_checker_with_invalid_url(caplog):
    try:
        url = "not_even_http"
        url_checker(url=url)
        assert False
    except:
        assert f"Invalid url: {url}" in caplog.messages
        assert True


def test_url_checker_with_a_valid_url(caplog):
    try:
        url = "https://this.should.work"
        url_checker(url=url)
        assert True
    except:
        assert False
