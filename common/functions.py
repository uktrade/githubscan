# -*- coding: utf-8 -*-
import json
import logging
import re

import requests

from common.models import JsonStore

logger = logging.getLogger(__name__)

email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
)


def write_to_json_store(data, field):
    """
    Function to Write data to given text field in JsonStore

    Parameters:
    -----------
    data = Dict
    field = name of the field
    """

    isinstance_of(variable=data, expected_type=dict, variable_name="data")

    table_fields = [table_field.name for table_field in JsonStore()._meta.get_fields()]

    if field not in table_fields:
        message = f"{field} does not exist in JsonStore"
        logger.error(message)
        raise KeyError(message)

    try:
        data_store = JsonStore.objects.get(id=1)
    except JsonStore.DoesNotExist:
        JsonStore(id=1).save()

    data_store = JsonStore.objects.get(id=1)

    setattr(
        data_store,
        field,
        json.dumps(data, default=lambda o: o.__dict__, sort_keys=True),
    )

    data_store.save()
    logger.info(f"added data to field {field}")


def read_from_json_store(field):
    """
    Function to read data to given text field in JsonStore

    Parameters:
    -----------
    data = Dict
    field = name of the field
    """

    table_fields = [table_field.name for table_field in JsonStore()._meta.get_fields()]

    if field not in table_fields:
        message = f"{field} does not exist in JsonStore"
        logger.error(message)
        raise KeyError(message)

    try:
        data_store = JsonStore.objects.get(id=1)

    except JsonStore.DoesNotExist:
        message = "No data in the table JsonStore"
        logger.error(message)
        raise

    content = json.loads(getattr(data_store, field))

    logger.info(f"fetched data from field {field}")

    return content


def download_data(url, verify_ssl=True):
    """
    Download file and retrun data

    Parameters:
    -----------
    url: str. Download file URL
    verify_ssl: Bool. If SSL verification should be used or not

    Returns:
    --------
    dict object with file content
    """
    try:
        session = requests.session()

        response = session.get(url=url, verify=verify_ssl)

        if response.status_code != 200:
            logger.error(f"Download failed: {url}")
            raise

        return response.json()
    except:
        raise


def url_checker(url):
    """this regex can be improved a lot!"""
    url_regex = re.compile(r"^(https://|http://)")

    isinstance_of(variable=url, expected_type=str, variable_name="url")

    if not url_regex.match(url):
        message = f"Invalid url: {url}"
        logger.error(message)
        raise Exception(message)


# Not tested
def singleton(cls):
    """
    Function to be used as decorator to create a singletone class

    Parameters:
    ------------
    cls: class to be made singletone
    """
    instances = {}

    def getinstance():
        if cls not in instances:
            instances[cls] = cls()
        return instances[cls]

    return getinstance


def isinstance_of(variable, expected_type, variable_name):
    if not isinstance(variable_name, str):
        error_msg = f"variable_name expected to be str type but is {type(variable_name).__name__}"
        logger.info(error_msg)
        raise TypeError(error_msg)

    """
    Reason why we are inplementing instance_of is, built-in isinstance would identify
    both date and,datetime as identical and, it does not provide way to
    enforce direct mapping

    Document: https://docs.python.org/3/library/functions.html#isinstance
    """
    if variable.__class__.__name__ != expected_type.__name__:
        error_msg = f"{variable_name} expected to be {expected_type.__name__} type but is {type(variable).__name__}"
        logger.info(error_msg)
        raise TypeError(error_msg)

    return True


def isempty_string(variable, variable_name):
    """
    ensure whay we have got is a of type string
    """
    isinstance_of(variable, str, variable_name)

    if not variable:
        message = f"{variable_name} must be set"
        logger.info(message)
        raise ValueError(message)

    return True


def is_valid_email(email):
    global email_regex

    if re.fullmatch(email_regex, email):
        return True

    return False
