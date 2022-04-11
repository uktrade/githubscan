# -*- coding: utf-8 -*-
def test_gh_query_executor_api_client_empty(gh_query_executor, caplog):
    try:
        gh_query_executor.clear()
        gh_query_executor.api_client
        assert False
    except TypeError:
        assert (
            "api_client expected to be GHAPIClient type but is NoneType"
            in caplog.messages
        )
        assert True


def test_gh_query_executor_api_client_set_to_wrong_type(
    gh_query_executor, gh_query_builder, caplog
):
    try:
        gh_query_executor.api_client = gh_query_builder
        assert False
    except:
        gh_query_executor.clear()
        gh_query_builder.clear()
        assert (
            "api_client expected to be GHAPIClient type but is GHQueryBuilder"
            in caplog.messages
        )
        assert True


def test_gh_query_executor_api_client_sucess(gh_query_executor, gh_client):
    gh_query_executor.api_client = gh_client

    assert gh_query_executor.api_client == gh_client

    gh_query_executor.clear()
    gh_client.clear()
