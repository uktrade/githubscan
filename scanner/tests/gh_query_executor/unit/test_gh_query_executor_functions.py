# -*- coding: utf-8 -*-
from django.conf import settings
from pathlib import Path
from copy import deepcopy

QUERY_VARIABLES = {
    "login": settings.GITHUB_LOGIN,
    "first": settings.GITHUB_FIRST_N_RECORDS,
}


def test_gh_query_executor_teams_getter_when_empty(gh_query_executor):
    assert gh_query_executor.teams == []


def test_gh_query_executor_repositories_and_alerts_getter_when_empty(gh_query_executor):
    assert gh_query_executor.repositories_and_alerts == []


def test_gh_query_executor_team_repositories_getter_when_empty(gh_query_executor):
    assert gh_query_executor.repositories_and_alerts == []


"""
This tests simply checks if we get response, it can not check if response is expected or not
however it does ensure response is not an error
"""


def test_gh_query_executor_teams_setter(
    real_test, gh_query_executor, live_gh_client, gh_query_builder
):

    gh_query_executor.api_client = live_gh_client
    gh_query_executor.query_builder = gh_query_builder

    gh_query_builder.make_gql_query_from_file = Path.joinpath(
        gh_query_executor.QUERY_DIRECTORY, "teams.query.graphql"
    )
    gh_query_executor.teams_query = {
        "query": gh_query_builder.gql_query,
        "variables": deepcopy(QUERY_VARIABLES),
    }

    assert gh_query_executor.teams
    assert len(gh_query_executor.teams) >= 1

    gh_query_builder.clear()
    gh_query_executor.clear()


def test_gh_query_executor_repositories_and_alerts_setter(
    real_test, gh_query_executor, live_gh_client, gh_query_builder
):

    gh_query_executor.api_client = live_gh_client
    gh_query_executor.query_builder = gh_query_builder

    gh_query_builder.make_gql_query_from_file = Path.joinpath(
        gh_query_executor.QUERY_DIRECTORY, "repositories_info.query.graphql"
    )

    gh_query_executor.repositories_and_alerts_query = {
        "query": gh_query_builder.gql_query.replace("{$user}", settings.GITHUB_LOGIN),
        "variables": deepcopy(QUERY_VARIABLES),
    }

    assert gh_query_executor.repositories_and_alerts

    assert len(gh_query_executor.repositories_and_alerts) >= 1

    gh_query_builder.clear()
    gh_query_executor.clear()


def test_gh_query_executor_team_repositories_setter(
    real_test, gh_query_executor, live_gh_client, gh_query_builder
):
    """teams is a dependency of team_repositories"""

    gh_query_executor.api_client = live_gh_client
    gh_query_executor.query_builder = gh_query_builder

    gh_query_builder.make_gql_query_from_file = Path.joinpath(
        gh_query_executor.QUERY_DIRECTORY, "teams.query.graphql"
    )

    gh_query_executor.teams_query = {
        "query": gh_query_builder.gql_query,
        "variables": deepcopy(QUERY_VARIABLES),
    }

    gh_query_builder.clear()

    gh_query_builder.make_gql_query_from_file = Path.joinpath(
        gh_query_executor.QUERY_DIRECTORY, "team_repositories.query.graphql"
    )

    gh_query_executor.teams_repositories_query = {
        "query": gh_query_builder.gql_query,
        "variables": deepcopy(QUERY_VARIABLES),
    }

    assert gh_query_executor.teams_repositories
    assert len(gh_query_executor.teams_repositories) >= 1

    gh_query_builder.clear()
    gh_query_executor.clear()
