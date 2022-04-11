# -*- coding: utf-8 -*-
def test_payload_is_not_a_string(web_request, caplog):
    try:
        web_request.auth_header = web_request.token_auth_header
        web_request.auth_token = "some token"
        web_request.post_query = {"payload": "this will not work"}
        assert False
    except TypeError:
        web_request.clear()
        assert "payload expected to be str type but is dict" in caplog.messages
        assert True


def test_payload_is_empty(web_request, caplog):
    web_request.auth_header = web_request.token_auth_header
    web_request.auth_token = "some token"
    web_request.url = "https://httpbin.org/post"
    web_request.post_query = ""
    web_request.clear()
    assert f"Success: Post Query Response status: 200" in caplog.messages
