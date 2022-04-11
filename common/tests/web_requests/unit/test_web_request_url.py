# -*- coding: utf-8 -*-
def test_web_request_url_is_empty_string(web_request, caplog):
    try:
        web_request.url = ""
        assert False
    except ValueError:
        web_request.clear()
        assert "url must be set" in caplog.messages
        assert True


def test_web_request_url_is_None(web_request, caplog):
    try:
        web_request.url = None
        assert False
    except TypeError:
        web_request.clear()
        assert "url expected to be str type but is NoneType" in caplog.messages
        assert True


def test_web_request_url_is_invalid(web_request, caplog):
    try:
        invalid_url = "this_is_not_going_to_work"
        web_request.url = invalid_url
        assert False
    except Exception:
        web_request.clear()
        assert f"Invalid url: {invalid_url}" in caplog.messages
        assert True


def test_web_request_url_is_valid(web_request):
    valid_url = "https://this.is.ok"
    web_request.url = valid_url
    assert web_request.url == valid_url
