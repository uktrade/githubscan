# -*- coding: utf-8 -*-
from common.functions import isempty_string


def test_exception_1_variable_is_not_string(caplog):
    try:
        var = 10
        isempty_string(variable=var, variable_name="var")
        assert False
    except TypeError:
        assert "var expected to be str type but is int" in caplog.messages
        assert True


def test_exception_1_variable_is_empty(caplog):
    try:
        var = ""
        isempty_string(variable=var, variable_name="var")
        assert False
    except ValueError:
        assert "var must be set" in caplog.messages
        assert True


def test_success_isempty_string():
    var = "not an empty string"
    assert isempty_string(variable=var, variable_name="var")
