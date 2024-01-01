# -*- coding: utf-8 -*-
import pytest
from django.conf import settings

from scanner.gh_api_client import GHAPIClient
from scanner.gh_query_builder import GHQueryBuilder
from scanner.gh_query_executor import GHQueryExecutor


@pytest.fixture(scope="session")
def gh_client():
    gh_client = GHAPIClient(verify_ssl=True)
    yield gh_client
    gh_client.clear()


@pytest.fixture(scope="session")
def gh_query_builder():
    gh_query_builder = GHQueryBuilder()
    yield gh_query_builder
    gh_query_builder.clear()


@pytest.fixture(scope="session")
def gh_query_executor():
    gh_query_executor = GHQueryExecutor()
    yield gh_query_executor
    gh_query_executor.clear()


@pytest.fixture(scope="function")
def real_test(request):
    if settings.DEPLOYMENT_ENVIRONMENT != "real_test":
        pytest.skip(
            reason="These tests are against real endpoints, they needs a valid credentials and,are slow. if you want to run the, set DEPLOYMENT_ENVIRONMENT to 'real_test' in evironment"
        )


@pytest.fixture(scope="session")
def live_gh_client():
    """
    Create logged in api client for live testing
    """
    live_gh_client = GHAPIClient()
    live_gh_client.url = settings.GITHUB_API_URL
    live_gh_client.auth_header = live_gh_client.token_auth_header
    live_gh_client.auth_token = settings.GITHUB_AUTH_TOKEN

    yield live_gh_client

    live_gh_client.clear()
