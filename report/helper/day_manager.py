# -*- coding: utf-8 -*-
from datetime import datetime, date, timedelta
from config.date_formats import DATE_FORMAT
import logging
from common.functions import isinstance_of

logger = logging.getLogger(__name__)


class DayManager:
    """
    This class does following tasks
     - Convert Working days to Calendar days , given start date and number of calendar days
     - Convert Calendar days to Working days , given start date and number of working days
     - Calculate Work days between two given dates
     - Calculate Calender days between two given dates
     - Date before X number of working days
     - Date before X number of Calender days

     All of this is used in
      - calculating Escalation and Critical Breach
      - Warning User of up-coming Critical Breach
      - Generating test data for report
    """

    def __init__(self, uk_holidays):
        """
        Initalize Time with account for holidays data
        """
        self._uk_holidays = uk_holidays
        self._str_date_regex = datetime.strptime

    def clear(self):
        self._uk_holidays = []

    def __del__(self):
        self.clear()

    def _is_date(self, obj):
        isinstance_of(obj, date, "obj")
        return True

    def is_weekend_or_bank_holiday(self, day):
        """
        weekday count in datetime library is
        0: Monday
        1: Tuesday
        2: Wednesday
        3: Thursday
        4: Friday
        5: Saturday
        6: Sunday
        Thus weekday > 4 means weekend
        """

        self._is_date(obj=day)

        if day.weekday() > 4:
            return True

        if day in self._uk_holidays:
            return True

        return False

    def _str_to_date(self, str_date, format):
        """
        This uses strptime to
            - match format
            - raise error(s)
            - return date object if there are no errors
        """
        return self._str_date_regex(str_date, format).date()

    def str_date_to_date(self, date):
        """
        wrapper method to convert string date to date object
        No need to test this, we have already tested _str_to_date for all possible inputes
        """

        return self._str_to_date(date, DATE_FORMAT.DATE.value)

    def str_datetime_to_date(self, datetime):
        """
        wrapper method to convert string datetime to date object
        No need to test this, we have already tested _str_to_date for all possible inputes
        """
        return self._str_to_date(datetime, DATE_FORMAT.DATE_TIME.value)

    def date_to_str_date(self, date):
        """
        This uses strftime to
            - match format
            - raise error(s)
            - return date string if there are no errors
        """
        return datetime.strftime(date, DATE_FORMAT.DATE.value)

    def date_to_str_datetime(self, date):
        """
        This uses strftime to
            - match format
            - raise error(s)
            - return datetime string if there are no errors
        """
        return datetime.strftime(date, DATE_FORMAT.DATE_TIME.value)

    def calendar_days_between(self, start_date, end_date=date.today()):
        """
        Gets number of calendar days between two dates

        Paramters:
        ----------
        start_date: date object
        end_date: date object , defaults to today

        Returns:
        ---------
        Number of days between two dates ( counting start date to day before end date )
        i.e. start day 6th April 9th April () will count 6,7 and 8 which is 3 days
        """
        self._is_date(obj=start_date)
        self._is_date(obj=end_date)

        if start_date > end_date:
            raise ValueError("start date can not be after end date")

        return (end_date - start_date).days

    def business_days_between(self, start_date, end_date=date.today()):
        """
        Gets number of calendar days between two dates

        Paramters:
        ----------
        start_date: date object
        end_date: date object , defaults to today

        Returns:
        ---------
        Number of business days between two dates
        """
        self._is_date(start_date)
        self._is_date(end_date)

        if start_date > end_date:
            raise ValueError("start date can not be after end date")

        business_days = 0

        """
        adding day here reflect fact that normally when we count days
        we do not include start date and do include end date.
        """
        day = start_date + timedelta(days=1)

        while day <= end_date:
            if not self.is_weekend_or_bank_holiday(day):
                business_days += 1

            day += timedelta(days=1)

        return business_days

    def date_before_n_business_days(self, end_date=date.today(), business_days=0):
        """
        This method counts backwards to get the start date
        given endate and number of business days. This method is used to generate
        mock data for testing purpose

        Parameters:
        -----------
        end_date: date object , defaults to today
        business_days: int number of business days to go back , defaults to 0

        Returns:
        --------
        date object with starting date ( used in createdAt filed in mock test data)
        """

        self._is_date(obj=end_date)

        isinstance_of(business_days, int, "business_days")

        start_date = end_date
        while business_days > 0:
            while self.is_weekend_or_bank_holiday(day=start_date):
                start_date -= timedelta(days=1)
                continue

            business_days -= 1
            start_date -= timedelta(days=1)

            while self.is_weekend_or_bank_holiday(day=start_date):
                start_date -= timedelta(days=1)

        return start_date

    def business_days_to_calendar_days(self, start_date, business_days=0):
        """
        converts N number of business days to calendar days, given start date

        Paramters:
        ----------
        start_date : date object, date from which we shouod count
        business_days: number of business days to account for

        Note: we do not count from start date but day after to be in line with datetime library
        i.e. in datetime library 01/01/01 + 5 days = 06/01/01 not 05/01/01
        """
        calendar_days = 0

        self._is_date(obj=start_date)

        isinstance_of(business_days, int, "business_days")

        """
        Move start date by one day and start accounting from that day onwards
        """
        start_date += timedelta(days=1)
        while business_days:

            if not self.is_weekend_or_bank_holiday(start_date):
                business_days -= 1

            calendar_days += 1
            start_date += timedelta(days=1)

        return calendar_days

    def end_date(self, start_date, calendar_days=0):
        """
        This method is used in generating test data

        Paramtertes:
        ------------
        start_date: date object
        calender_days: int object

        Returns:
        --------
        date object
        """

        self._is_date(obj=start_date)

        isinstance_of(calendar_days, int, "calendar_days")

        return start_date + timedelta(days=calendar_days)

    def working_days_between_dates(self, end_date, start_date=date.today()):

        working_days = 0
        """
        if start date is before end date
        """
        if start_date < end_date:
            if self.is_weekend_or_bank_holiday(start_date):
                working_days += 1

            while start_date != end_date:
                if self.is_weekend_or_bank_holiday(start_date):
                    start_date += timedelta(days=1)
                    continue

                working_days += 1
                start_date += timedelta(days=1)

        """
        if start date is after end date , in other worlds
        end date is already reached and we want to find out
        how many days we are adding to delay
        """
        if start_date > end_date:
            while start_date != end_date:
                if self.is_weekend_or_bank_holiday(start_date):
                    start_date -= timedelta(days=1)
                    continue

                working_days -= 1
                start_date -= timedelta(days=1)

        return working_days
