# -*- coding: utf-8 -*-
import logging
from datetime import datetime

from common.functions import download_data, isinstance_of, url_checker
from config.date_formats import DATE_FORMAT

logger = logging.getLogger(__name__)


class UKHolidays:

    """
    As name suggest it gets uk holidays data
    It also downloads those data to a file and, uses it until max threshold is passed
    """

    def __init__(self, verify_ssl=True):
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
        isinstance_of(verify_ssl, bool, "verify_ssl")

        self._holidays = []
        self._verify_ssl = verify_ssl

        logger.debug(f"Initialized {self.__class__.__name__}")

    def clear(self):
        self._holidays = []

    def __del__(self):
        self.clear()

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

        url_checker(url=url)
        holidays_data = download_data(url=url, verify_ssl=self._verify_ssl)

        if "england-and-wales" not in holidays_data.keys():
            message = "missing england-and-wales key from data"
            logger.error(message)
            raise KeyError(message)

        self._holidays = [
            datetime.strptime(event["date"], DATE_FORMAT.DATE.value).date()
            for event in holidays_data["england-and-wales"]["events"]
        ]
        logger.debug("Success: processed uk holidays data")
