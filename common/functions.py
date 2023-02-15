# -*- coding: utf-8 -*-
import json
import logging
import requests
import re
import time
import traceback

logger = logging.getLogger(__name__)

email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])"
)


def write_json_file(data, dest_file):
    """
    Function to create/over-write Json file

    Parameters:
    -----------
    data = Dict
    dest_file = PosixPath
    """

    isinstance_of(variable=data, expected_type=dict, variable_name="data")

    try:
        with open(dest_file, "w") as file:
            file.truncate(0)
            content = json.dumps(
                data, default=lambda o: o.__dict__, sort_keys=True, indent=2
            )
            file.write(content)
            logger.info(f"created {dest_file}")
            file.close()
    except:
        logger.error(f"failed to create {dest_file}")
        file.close()
        raise


def load_json_file(src_file):
    """
    Function to load json file and return python dict

    Parameter:
    ----------
    src_file: PosixPath

    Returns:
    --------
    python dict object
    """

    try:
        with open(src_file) as file:
            data = json.load(file)
            file.close()
            logger.info(f"loaded data from {src_file}")
            return data
    except Exception as e:
        logger.error(f"{e}")
        file.close()
        raise


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


def command_runner(command_name):
    """
    A decorator function which can be used with Django command handle function
    It will time it and print useful logging informationa s of now
    However, it can be expanded to  add status page and more

    command_name: this parameter makes it easy to identify which command is being executed
    """

    def inner_command(handle):
        def wrapper(self, *args, **option):
            try:
                start_time = time.time()

                handle()
                end_time = time.time()

                logger.info(f"Time: {end_time - start_time}s Success: {command_name}")
            except Exception as e:

                end_time = time.time()
                logger.info(
                    f"Time: {end_time - start_time}s {command_name.capitalize()} Error: {e}"
                )
                print(
                    f"Execustion Time: {end_time - start_time}s {command_name.capitalize()} Error:{format(e)}"
                )
                logger.info(f"Error Trace: {traceback.print_exc()}")

        return wrapper

    return inner_command


def job_runner(command_name, function):
    """
    A  function which can be used with any function to time it and print useful logging informationa
    However, it can be expanded to  add status page and more

    command_name: this parameter makes it easy to identify which command is being executed
    function: is the actual function to execute
    """

    try:
        start_time = time.time()

        function()
        end_time = time.time()

        logger.info(f"Time: {end_time - start_time}s Success: {command_name}")
    except Exception as e:

        end_time = time.time()
        logger.info(
            f"Time: {end_time - start_time}s {command_name.capitalize()} Error: {e}"
        )
        print(
            f"Execustion Time: {end_time - start_time}s {command_name.capitalize()} Error:{format(e)}"
        )
        logger.info(f"Error Trace: {traceback.print_exc()}")


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
