# -*- coding: utf-8 -*-
import logging
from datetime import datetime
from pathlib import PosixPath

from common.functions import (
    download_data,
    isinstance_of,
    load_json_file,
    url_checker,
    write_json_file,
)
from config.date_formats import DATE_FORMAT

logger = logging.getLogger(__name__)


class UKHolidays:

    """
    As name suggest it gets uk holidays data
    It also downloads those data to a file and, uses it until max threshold is passed
    """

    def __init__(self, data_file, max_data_file_age, verify_ssl=True):
        """
        Parameters:
        -----------
        verify_ssl: sets if ssl should be used while getting data file
        data_file: PoxiPath , File to which holidays data will be dumped and read from
        max_data_file_age: max time in days, after that file would be updated with fresh content

        Variables:
        ----------
        self._holidays: list of events in England and Walse
        self._verify_ssl: Bool , Defaukts to true
        self._data_file: same as param data_file
        self._max_data_file_age: same as max_data_file_age
        """

        isinstance_of(data_file, PosixPath, "data_file")
        isinstance_of(max_data_file_age, int, "max_data_file_age")
        isinstance_of(verify_ssl, bool, "verify_ssl")

        self._holidays = []
        self._verify_ssl = verify_ssl
        self._data_file = data_file
        self._max_data_file_age = max_data_file_age

        logger.debug(f"Initialized {self.__class__.__name__}")

    def clear(self):
        self._holidays = []

    def __del__(self):
        self.clear()

    @property
    def uk_holidays_file(self):
        """
        Return the file path of current holidays file
        """
        return self._data_file

    @property
    def uk_holidays_file_max_age(self):
        """
        Returns the max allowed age of holidays file
        """
        return self._max_data_file_age

    @property
    def calendar(self):
        if not self._holidays:
            logger.debug(f"there are no data in holidays, have you set the setter?")
        return self._holidays

    @calendar.setter
    def calendar_url(self, url):
        """
        Get holidays data from data source and, filter them to events for
        England and Walse
        """

        if self._should_download_file:
            url_checker(url=url)
            data = download_data(url=url, verify_ssl=self._verify_ssl)

            if "england-and-wales" not in data.keys():
                message = "missing england-and-wales key from data"
                logger.error(message)
                raise KeyError(message)

            write_json_file(data=data, dest_file=self._data_file)

        data_from_file = load_json_file(src_file=self._data_file)

        self._holidays = [
            datetime.strptime(event["date"], DATE_FORMAT.DATE.value).date()
            for event in data_from_file["england-and-wales"]["events"]
        ]
        logger.debug("Success: processed uk holidays data")

    @property
    def _should_download_file(self):
        """
        Figure out if we should download new file or not
        If file exists, we need to check the age
        """

        if self._data_file.exists():
            file_age = datetime.today() - datetime.fromtimestamp(
                self._data_file.stat().st_mtime
            )
            logger.debug(f"File is {file_age.days} days old")
            if file_age.days < self._max_data_file_age:
                return False

        logger.debug(f"FileNotFound:{self._data_file}")
        return True
