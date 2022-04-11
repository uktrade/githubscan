# -*- coding: utf-8 -*-
import os
from datetime import datetime, timedelta


def test_when_file_does_not_exist(uk_holidays):
    try:
        assert uk_holidays._should_download_file == True
        assert True
    except:
        assert False


def test_when_file_exist_and_age_is_less_than_max_age(uk_holidays):
    try:
        with open(uk_holidays.uk_holidays_file, "w") as file:
            file.write("testing")

        assert uk_holidays._should_download_file == False
        assert True

        uk_holidays.uk_holidays_file.unlink()

    except:
        assert False


def test_when_file_exist_and_age_is_more_than_max_age(uk_holidays):
    try:
        """
        Crete file
        """
        with open(uk_holidays.uk_holidays_file, "w") as file:
            file.write("testing")

        """ Set Access and modified time to  2 days plus max age"""
        dt_epoc = (
            datetime.now() - timedelta(days=uk_holidays.uk_holidays_file_max_age + 2)
        ).timestamp()

        os.utime(uk_holidays.uk_holidays_file, (dt_epoc, dt_epoc))

        assert uk_holidays._should_download_file == True
        assert True
        uk_holidays.uk_holidays_file.unlink()
    except:
        assert False
