# -*- coding: utf-8 -*-


from enum import Enum


class DATE_FORMAT(Enum):
    """
    Enum to Specify the Date and time formats
    DATE:str represents YYYY-MM-DD
    DATE_TIME:str reprents YYYY-MM-DDTHH:MM:SSZ
    """

    DATE = "%Y-%m-%d"
    DATE_TIME = "%Y-%m-%dT%H:%M:%SZ"
