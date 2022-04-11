# -*- coding: utf-8 -*-
from common.functions import download_data
from django.conf import settings


def test_invalid_url(caplog):
    try:
        URL = "https://www.gov.uk/no-bank-holidays.json"
        download_data(url=URL)
        assert False
    except:
        assert f"Download failed: {URL}" in caplog.messages
        assert True


def test_valid_url():
    try:
        data = download_data(url=settings.UK_HOLIDAYS_SOURCE_URL)
        assert data
        assert len(data) >= 1
        assert True
    except:
        assert False
