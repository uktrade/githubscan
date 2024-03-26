# -*- coding: utf-8 -*-
from pathlib import Path

from django.conf import settings

from common.functions import read_from_json_store, write_to_json_store
from config.schema import scanner_data_schema
from scanner.gh_api_client import GHAPIClient
from scanner.gh_query_builder import GHQueryBuilder
from scanner.gh_query_executor import GHQueryExecutor


def create_scanner_data():
    """
    This function Use of following classes to build and execute query
     - GHQueryBuilder
     - GHQueryExecutor
    """

    scanner_data = {
        "enterprise_users": {},
        "repositories": [],
        "teams": [],
        "team_repositories": [],
        "team_members": {},
    }

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
    # Enterprise users
    query_builder.make_gql_query_from_file = Path.joinpath(
        query_executor.QUERY_DIRECTORY, "enterprise_users.query.graphql"
    )
    query_executor.enterprise_users = {
        "query": query_builder.gql_query,
        "variables": dict(QUERY_VARIABLES),
    }
    # Teams
    query_builder.make_gql_query_from_file = Path.joinpath(
        query_executor.QUERY_DIRECTORY, "teams.query.graphql"
    )
    query_executor.teams_query = {
        "query": query_builder.gql_query,
        "variables": dict(QUERY_VARIABLES),
    }
    # Team members
    query_builder.make_gql_query_from_file = Path.joinpath(
        query_executor.QUERY_DIRECTORY, "team_members.query.graphql"
    )
    query_executor.team_members_query = {
        "query": query_builder.gql_query,
        "variables": dict(QUERY_VARIABLES),
    }
    # Repository info/alerts
    query_builder.make_gql_query_from_file = Path.joinpath(
        query_executor.QUERY_DIRECTORY, "repositories_info.query.graphql"
    )
    query_executor.repositories_and_alerts_query = {
        "query": query_builder.gql_query.replace("{$user}", settings.GITHUB_LOGIN),
        "variables": dict(QUERY_VARIABLES),
    }
    # Team repositories
    query_builder.make_gql_query_from_file = Path.joinpath(
        query_executor.QUERY_DIRECTORY, "team_repositories.query.graphql"
    )
    query_executor.teams_repositories_query = {
        "query": query_builder.gql_query,
        "variables": dict(QUERY_VARIABLES),
    }
    scanner_data["enterprise_users"] = query_executor.enterprise_users
    scanner_data["orphan_sso_emails"] = query_executor.orphan_sso_emails
    scanner_data["invalid_emails"] = query_executor.invalid_emails
    scanner_data["repositories"] = query_executor.repositories_and_alerts
    scanner_data["teams"] = query_executor.teams
    scanner_data["team_repositories"] = query_executor.teams_repositories
    scanner_data["team_members"] = query_executor.team_members
    scanner_data_schema.validate(scanner_data)
    api_client.clear()
    query_builder.clear()
    query_executor.clear()
    return scanner_data


def write_scanner_data(scanner_data, dest_field=settings.SCANNER_DATA_FIELD_NAME):
    """
    create file containing scanner data

    Parameters:
    -----------
    scanner_data: dict object generated using create_scanner_data()
    dest_file: Posix ( or str) Path to the scanner data file , defaults to settings.SCANNER_DATA_FIELD_NAME variable defined in environment
    """

    scanner_data_schema.validate(scanner_data)
    write_to_json_store(data=scanner_data, field=dest_field)


def read_scanner_data(dest_field=settings.SCANNER_DATA_FIELD_NAME):
    """
    create file containing scanner data

    Parameters:
    -----------
    dest_file: Posix ( or str) Path to the scanner data file , defaults to settings.SCANNER_DATA_FIELD_NAME variable defined in environment
    """
    scanner_data = read_from_json_store(field=dest_field)
    return scanner_data


def refresh_scan():
    """
    Sends queries to github end point to collect data and
    write data to scanner file

    Note: Not tested , needs integration testing ?
    """
    scanner_data = create_scanner_data()
    write_scanner_data(scanner_data=scanner_data)
