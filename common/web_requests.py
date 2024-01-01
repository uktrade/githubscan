# -*- coding: utf-8 -*-
import logging

import requests

from common.functions import isempty_string, isinstance_of, url_checker

logger = logging.getLogger(__name__)


class WebRequests:
    """
    A simple wrapper to requests library which
     - authenticates against given api end point
     - POST the requested payload
    """

    def __init__(self, verify_ssl=True):
        """
        Initalize values to be used with class

        Parameters:
        -----------
        url : str. you must provide this parameter
        verify_ssl: boolean. defaults to true

        Variables: All variables here are private and used internally by class
        ----------
        self._session : variable to hold session context
        self._response : dict. this varialbe holds the response from api server
        self._url : str
        self._verify_ssl: boolean , default to True
        self._auth_header: sets auth header with token or bearer
        self._token: keeps token handy
        """
        isinstance_of(verify_ssl, bool, "verify_ssl")
        self._url = ""
        self._verify_ssl = verify_ssl
        self._session = requests.session()
        self._response = {}
        self._auth_header = {}
        self._token = ""

    def clear(self):
        """
        Method to  clear values  from all class variables
        """
        self._url = ""
        self._response = {}
        self._response = {}
        self._auth_header = {}
        self._token = ""

    def __del__(self):
        """
        Destroctor: Method called when object id destroyed
        it simply claer all variables
        """
        self.clear()

    def _is_valid_header(self, header):
        if not (header == self.token_auth_header or header == self.bearer_auth_header):
            message = "auth_header must be set to token or Bearer type"
            logger.info(message)
            raise ValueError("message")

    @property
    def url(self):
        isempty_string(self._url, "url")
        return self._url

    @url.setter
    def url(self, end_point):
        isempty_string(end_point, "url")
        url_checker(end_point)
        self._url = end_point

    @property
    def verify_ssl(self):
        return self._verify_ssl

    @verify_ssl.setter
    def verify_ssl(self, verify_ssl):
        isinstance_of(verify_ssl, bool, "verify_ssl")
        self._verify_ssl = verify_ssl

    @property
    def token_auth_header(self):
        return {
            "Authorization": "token ",
            "Content-Type": "application/json; charset=utf-8",
        }

    @property
    def bearer_auth_header(self):
        return {
            "Authorization": "Bearer ",
            "Content-Type": "application/json; charset=utf-8",
        }

    @property
    def auth_header(self):
        """
        returns auth header
        """
        isinstance_of(self._auth_header, dict, "auth_header")

        if not self._token:
            self._is_valid_header(header=self._auth_header)

        """ we need a way to mask token in logs here """
        return self._auth_header

    @auth_header.setter
    def auth_header(self, auth_header):
        isinstance_of(auth_header, dict, "auth_header")
        self._is_valid_header(header=auth_header)
        self._auth_header = auth_header

    @property
    def post_response(self):
        """Returns current reqest repose"""
        return self._response

    def auth_token(self, token):
        """
        This method sets token to header

        Paramters:
        ----------
        token: str. You must supply the github token here and it must not be empty
        """

        isinstance_of(token, str, "auth_token")

        isempty_string(token, "auth_token")

        self._token = token

        self._is_valid_header(header=self.auth_header)

        self.auth_header["Authorization"] += token

        logger.info("auth_token is set")

    auth_token = property(None, auth_token)

    @post_response.setter
    def post_query(self, payload):
        """
        This method sets response to request

        Parameter:
        -----------
        payload: str, it should be string object
        """

        isinstance_of(payload, str, "payload")

        """
        Ensure Auth Token is set before we post request
        """

        try:
            self._session.headers = self.auth_header
            self._response = self._session.post(
                self.url, data=payload, verify=self.verify_ssl
            )

            content = self.post_response.json()

            if "errors" in content:
                logger.info(f'Errors: {content["errors"]}')
                raise Exception(content["errors"])

            if "error" in content:
                logger.info(f'Error: {content["error"]}')
                raise Exception(content["error"])

            logger.debug(
                f"Success: Post Query Response status: {self.post_response.status_code}"
            )

        except:
            if self.post_response:
                logger.info(
                    f"Failed: Post Query Response status: {self.post_response.status_code}"
                )
                logger.debug(f"Error: {self.post_response.content}")

            raise
