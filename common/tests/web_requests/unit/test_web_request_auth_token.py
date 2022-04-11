# -*- coding: utf-8 -*-


def test_web_request_set_auth_token_empty(web_request, caplog):
    try:
        web_request.auth_token = ""
        assert False
    except ValueError:
        web_request.clear()
        assert f"auth_token must be set" in caplog.messages
        assert True


def test_web_request_set_auth_token_integer(web_request, caplog):
    try:
        web_request.auth_token = 10
        assert False
    except TypeError:
        web_request.clear()
        assert f"auth_token expected to be str type but is int" in caplog.messages
        assert True


def test_web_request_exception_auth_token_is_not_set(web_request, caplog):
    try:
        web_request.auth_token = ""
        assert False
    except ValueError:
        web_request.clear()
        assert "auth_token must be set" in caplog.messages
        assert True


def test_web_request_set_auth_token_does_not_set_without_header(web_request, caplog):
    try:
        token = "my_auth_token"
        web_request.auth_token = token
        assert False
    except ValueError:
        web_request.clear()
        assert "auth_header must be set to token or Bearer type" in caplog.messages
        assert True


def test_web_request_set_auth_token_success_with_token_header(web_request):
    try:
        token = "my_auth_token"
        web_request.auth_header = web_request.token_auth_header
        web_request.auth_token = token
        web_request.clear()
        assert True
    except ValueError:
        assert False


def test_web_request_set_auth_token_success_with_bearer_header(web_request):
    try:
        token = "my_auth_token"
        web_request.auth_header = web_request.bearer_auth_header
        web_request.auth_token = token
        web_request.clear()
        assert True
    except ValueError:
        assert False
