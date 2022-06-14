# -*- coding: utf-8 -*-
import pytest
from common.web_requests import WebRequests


@pytest.fixture(scope="session")
def web_request():
    web_request = WebRequests(verify_ssl=True)
    yield web_request
    web_request.clear()
