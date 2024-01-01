# -*- coding: utf-8 -*-
import json
import logging

from common.functions import isinstance_of

logger = logging.getLogger(__name__)


class GHQueryBuilder:
    def __init__(self):
        self._query_text = ""

    def clear(self):
        self._query_text = ""

    def __del__(self):
        self.clear()

    @property
    def gql_query(self):
        """Simply returns the loaded graphql query text"""
        logger.debug(f"Query_text: {self._query_text}")
        return self._query_text

    @gql_query.setter
    def make_gql_query_from_file(self, query_file):
        """
        This method converts query file to string in acceptable format

        Paramters:
        ----------
        query_file: PosixPath ( but could be string too since, open() accepts either)
        """
        try:
            content = ""
            with open(query_file, "r", encoding="unicode_escape") as file:
                content = file.read().splitlines()

            self._query_text = "".join(str(c) for c in content)

        except:
            logger.info(f"Failed to load {query_file}")
            raise

    @gql_query.setter
    def make_gql_query_from_dict(self, query_dict):
        isinstance_of(query_dict, dict, "query_dict")
        self._query_text = json.dumps(query_dict)

    def is_a_valid_input_query(self, payload, caller="(PUT_CALLER_NAME_HERE)"):
        """
        Validates that supplied query payload is in expected format and has expected keys
        Also, a Private method intended to used by the specific query executor functions
        Paramters:
        ----------
        caller: str. simply name of the calling function ( we do so manually at the moment). it defaults to (PUT_CALLER_NAME_HERE)
        payload: dict. dictionay of query and query variables
        """

        isinstance_of(payload, dict, "payload")

        if "query" not in payload.keys() or "variables" not in payload.keys():
            message = f"{caller} query missing expected keys, both query and variables key should be supplied"
            logger.error(message)
            raise ValueError(message)

        isinstance_of(payload["query"], str, 'payload["query"]')
        isinstance_of(payload["variables"], dict, 'payload["variables"]')

        return True
