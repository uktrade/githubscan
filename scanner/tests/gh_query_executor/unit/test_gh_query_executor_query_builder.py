# -*- coding: utf-8 -*-
def test_gh_query_executor_query_builder_empty(gh_query_executor, caplog):
    try:
        gh_query_executor.clear()
        gh_query_executor.query_builder
        assert False
    except TypeError:
        assert (
            "query_builder expected to be GHQueryBuilder type but is NoneType"
            in caplog.messages
        )
        assert True


def test_gh_query_executor_query_builder_set_to_wrong_type(
    gh_query_executor, gh_client, caplog
):
    try:
        gh_query_executor.query_builder = gh_client
        assert False
    except:
        gh_query_executor.clear()
        gh_client.clear()
        assert (
            "query_builder expected to be GHQueryBuilder type but is GHAPIClient"
            in caplog.messages
        )
        assert True


def test_gh_query_executor_query_builder_sucess(gh_query_executor, gh_query_builder):
    gh_query_executor.query_builder = gh_query_builder

    assert gh_query_executor.query_builder == gh_query_builder

    gh_query_executor.clear()
    gh_query_builder.clear()
