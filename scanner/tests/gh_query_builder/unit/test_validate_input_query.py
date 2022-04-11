# -*- coding: utf-8 -*-
def test_exception_payload_is_not_a_dict(gh_query_builder, caplog):
    try:
        caller_name = "test_01"
        gh_query_builder.is_a_valid_input_query(
            payload="this query would not work", caller=caller_name
        )
        assert False
    except TypeError:
        assert f"payload expected to be dict type but is str" in caplog.messages
        assert True


def test_exception_payload_query_key_must_be_string(gh_query_builder, caplog):
    try:
        caller_name = "test_04"
        test_query = {"query": {}, "variables": {}}
        gh_query_builder.is_a_valid_input_query(caller=caller_name, payload=test_query)
        assert False
    except TypeError:
        assert (
            f'payload["query"] expected to be str type but is dict' in caplog.messages
        )
        assert True


def test_exception_payload_variables_key_must_be_dict(gh_query_builder, caplog):
    try:
        caller_name = "test_05"
        test_query = {"query": "query string", "variables": ""}
        gh_query_builder.is_a_valid_input_query(caller=caller_name, payload=test_query)
        assert False
    except TypeError:
        assert (
            f'payload["variables"] expected to be dict type but is str'
            in caplog.messages
        )
        assert True


def test_exception_payload_missing_variables_key(gh_query_builder, caplog):
    try:
        caller_name = "test_02"
        test_query = {"query": "my query string"}
        gh_query_builder.is_a_valid_input_query(caller=caller_name, payload=test_query)
        assert False
    except ValueError:
        assert (
            f"{caller_name} query missing expected keys, both query and variables key should be supplied"
            in caplog.messages
        )
        assert True


def test_exception_payload_missing_query_key(gh_query_builder, caplog):
    try:
        caller_name = "test_03"
        test_query = {"variables": {}}
        gh_query_builder.is_a_valid_input_query(caller=caller_name, payload=test_query)
        assert False
    except ValueError:
        assert (
            f"{caller_name} query missing expected keys, both query and variables key should be supplied"
            in caplog.messages
        )
        assert True


def test_valid_payload_with_caller(gh_query_builder):
    try:
        caller_name = "test_06"
        test_query = {"query": "my string", "variables": {}}
        gh_query_builder.is_a_valid_input_query(caller=caller_name, payload=test_query)
        gh_query_builder.clear()
        assert True
    except:
        assert False


def test_valid_payload_without_caller(gh_query_builder):
    try:
        test_query = {"query": "my string", "variables": {}}
        gh_query_builder.is_a_valid_input_query(payload=test_query)
        gh_query_builder.clear()
        assert True
    except:
        assert False
