# -*- coding: utf-8 -*-
from pathlib import Path


def test_empty_getter_response(gh_query_builder):
    gh_query_builder.gql_query == ""


def test_exception_make_query_from_non_existing_file(gh_query_builder, caplog):
    try:
        QUERY_FILE = Path.joinpath(
            Path(__file__).parent.parent,
            "fixtures",
            "this.query.graphql.is.not.there",
        )
        gh_query_builder.make_gql_query_from_file = QUERY_FILE
        assert False
    except FileNotFoundError:
        assert True
        assert gh_query_builder.gql_query == ""
        assert f"Failed to load {QUERY_FILE}" in caplog.messages


def test_make_query_from_file(gh_query_builder, caplog):
    QUERY_FILE = Path.joinpath(
        Path(__file__).parent.parent, "fixtures", "test.query.graphql"
    )
    gh_query_builder.make_gql_query_from_file = QUERY_FILE
    assert (
        gh_query_builder.gql_query
        == "query($login:String!){    organization(login:$login){        login        name    }}"
    )
    gh_query_builder.clear()


def test_exception_make_query_from_dict(gh_query_builder, caplog):
    try:
        gh_query_builder.make_gql_query_from_dict = "{ 'my': 'query' }"
        assert False
    except TypeError:
        assert True
        assert gh_query_builder.gql_query == ""
        assert f"query_dict expected to be dict type but is str" in caplog.messages


def test_make_query_from_dict(gh_query_builder):
    gh_query_builder.make_gql_query_from_dict = {"my": "query"}
    assert gh_query_builder.gql_query == '{"my": "query"}'
    gh_query_builder.clear()
