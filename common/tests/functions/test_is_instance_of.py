# -*- coding: utf-8 -*-
from common.functions import isinstance_of


def test_exception_01_incorrect_expectation(caplog):
    var = 10
    expected_type = str
    var_name = "var"

    try:
        isinstance_of(variable=var, expected_type=expected_type, variable_name=var_name)
        assert False
    except TypeError:
        assert f"var expected to be str type but is int" in caplog.messages
        assert True


def test_exception_02_variable_name_is_not_string(caplog):
    var = 10
    expected_type = str
    var_name = var

    try:
        isinstance_of(variable=var, expected_type=expected_type, variable_name=var)
        assert False
    except TypeError:
        assert f"variable_name expected to be str type but is int" in caplog.messages
        assert True


def test_success_isinsance_of():
    var = 10
    expected_type = int
    var_name = "var"
    assert isinstance_of(
        variable=var, expected_type=expected_type, variable_name=var_name
    )
