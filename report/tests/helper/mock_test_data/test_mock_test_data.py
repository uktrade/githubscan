# -*- coding: utf-8 -*-
from config.severities import SEVERITY_STATUS
from config.schema import scanner_data_schema


def test_mock_data_alerts_set_before_generating_set(mock_test_data):
    for key, value in mock_test_data.alert_sets.items():
        assert value == []


def test_mock_scenarios_before_generating_them(mock_test_data):
    assert mock_test_data.mock_scenarios == {}


def test_mock_test_alert_sets_properties(mock_test_data):
    mock_test_data.create_alerts_set()
    alert_sets = mock_test_data.alert_sets

    assert SEVERITY_STATUS.RED.name in alert_sets
    assert SEVERITY_STATUS.AMBER.name in alert_sets
    assert SEVERITY_STATUS.GREEN.name in alert_sets
    assert SEVERITY_STATUS.CLEAN.name in alert_sets
    assert len(alert_sets[SEVERITY_STATUS.RED.name]) == 4
    assert len(alert_sets[SEVERITY_STATUS.AMBER.name]) == 6
    assert len(alert_sets[SEVERITY_STATUS.GREEN.name]) == 4
    assert len(alert_sets[SEVERITY_STATUS.CLEAN.name]) == 1

    mock_test_data.clear()


def test_mock_scenarios_properties(mock_test_data):
    mock_test_data.create_alerts_set()
    mock_test_data.generate_scenarios()
    """ test number of scenarios should be 7"""
    assert len(mock_test_data.mock_scenarios) == 8

    """ assert number of keys in each mock data """
    for scene_index, scene_data in mock_test_data.mock_scenarios.items():
        assert len(scene_data.keys()) == 3

        clean_repositories_counter = 0

        for repository in scene_data["repositories"]:
            if not repository["alerts"]:
                clean_repositories_counter += 1

        if scene_index == 1:
            assert clean_repositories_counter == 1

        if scene_index == (2 or 5):
            assert clean_repositories_counter == 5

        if scene_index == 3:
            assert clean_repositories_counter == 7

        if scene_index == (4 or 7):
            assert clean_repositories_counter == 11

        if scene_index == 6:
            assert clean_repositories_counter == 9

        if scene_index == 8:
            assert clean_repositories_counter == 15

    assert scanner_data_schema.is_valid(scene_data)

    mock_test_data.clear()
