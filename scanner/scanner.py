# -*- coding: utf-8 -*-
from scanner import GHAPIClient, GHQueryBuilder, GHQueryExecutor
from django.conf import settings
from pathlib import Path
from config.schema import scanner_data_schema
from common.functions import write_json_file


def create_scanner_data():
    """
    This function Use of following classes to build and execute query
     - GHQueryBuilder
     - GHQueryExecutor
    """
    try:
        scanner_data = {"repositories": [], "teams": [], "team_repositories": []}

        """ This function fetched data and write it to file """
        QUERY_VARIABLES = {
            "login": settings.GITHUB_LOGIN,
            "first": settings.GITHUB_FIRST_N_RECORDS,
        }

        api_client = GHAPIClient()
        api_client.url = settings.GITHUB_API_URL
        api_client.auth_header = api_client.token_auth_header
        api_client.auth_token = settings.GITHUB_AUTH_TOKEN

        query_builder = GHQueryBuilder()

        query_executor = GHQueryExecutor()

        query_executor.api_client = api_client
        query_executor.query_builder = query_builder

        query_builder.make_gql_query_from_file = Path.joinpath(
            query_executor.QUERY_DIRECTORY, "teams.query.graphql"
        )
        query_executor.teams_query = {
            "query": query_builder.gql_query,
            "variables": dict(QUERY_VARIABLES),
        }

        query_builder.make_gql_query_from_file = Path.joinpath(
            query_executor.QUERY_DIRECTORY, "repositories_info.query.graphql"
        )
        query_executor.repositories_and_alerts_query = {
            "query": query_builder.gql_query.replace("{$user}", settings.GITHUB_LOGIN),
            "variables": dict(QUERY_VARIABLES),
        }

        query_builder.make_gql_query_from_file = Path.joinpath(
            query_executor.QUERY_DIRECTORY, "team_repositories.query.graphql"
        )
        query_executor.teams_repositories_query = {
            "query": query_builder.gql_query,
            "variables": dict(QUERY_VARIABLES),
        }

        scanner_data["repositories"] = query_executor.repositories_and_alerts
        scanner_data["teams"] = query_executor.teams
        scanner_data["team_repositories"] = query_executor.teams_repositories

        scanner_data_schema.validate(scanner_data)

        api_client.clear()
        query_builder.clear()
        query_executor.clear()
        return scanner_data
    except:
        raise


def write_scanner_data(scanner_data, dest_file=settings.SCANNER_DATA_FILE_PATH):
    """
    create file containing scanner data

    Parameters:
    -----------
    scanner_data: dict object generated using create_scanner_data()
    dest_file: Posix ( or str) Path to the scanner data file , defaults to settings.SCANNER_DATA_FILE_PATH variable defined in environment
    """
    try:
        scanner_data_schema.validate(scanner_data)
        write_json_file(data=scanner_data, dest_file=dest_file)
    except:
        raise


def refresh_scan(*args, **options):
    """
    Sends queries to github end point to collect data and
    write data to scanner file

    Note: Not tested , needs integration testing ?
    """
    scanner_data = create_scanner_data()
    write_scanner_data(scanner_data=scanner_data)
