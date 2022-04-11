# -*- coding: utf-8 -*-
def test_web_request_set_auth_header_when_not_set(web_request, caplog):
    try:
        web_request.auth_header
        assert False
    except ValueError:
        web_request.clear()
        assert "auth_header must be set to token or Bearer type" in caplog.messages


def test_web_request_set_auth_header_when_set_with_wrong_type(web_request, caplog):
    try:
        web_request.auth_header = {"key": "value"}
        assert False
    except ValueError:
        web_request.clear()
        assert "auth_header must be set to token or Bearer type" in caplog.messages


def test_web_request_set_auth_header_when_set_with_token_header(web_request, caplog):
    try:
        web_request.auth_header = web_request.token_auth_header
        web_request.clear()
        assert True
    except:
        assert False


def test_web_request_set_auth_header_when_set_with_bearer_header(web_request, caplog):
    try:
        web_request.auth_header = web_request.bearer_auth_header
        web_request.clear()
        assert True
    except:
        assert False
