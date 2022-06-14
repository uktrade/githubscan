# -*- coding: utf-8 -*-
from report.helper.functions import sort_dict_by_total


def test_sort_dict_by_total(data_index, processed_data):

    sorted_team_data = dict(sort_dict_by_total(data=processed_data, key="teams"))

    sorted_repository_data = dict(
        sort_dict_by_total(data=processed_data, key="repositories")
    )

    """
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """
    if data_index == 1:
        assert list(sorted_team_data.keys()) == ["team1", "team2", "team3", "team4"]
        assert list(sorted_repository_data.keys())[0] == "repository_01"

    if data_index == 3:
        assert list(sorted_team_data.keys()) == ["team1", "team3", "team2", "team4"]

    if data_index == 5:
        assert list(sorted_team_data.keys()) == ["team2", "team3", "team1", "team4"]
        assert list(sorted_repository_data.keys())[0] == "repository_05"

    if data_index == 6:
        assert list(sorted_team_data.keys()) == ["team2", "team1", "team3", "team4"]
        assert list(sorted_repository_data.keys())[0] == "repository_05"

    if data_index == 7:
        assert list(sorted_team_data.keys()) == ["team3", "team1", "team2", "team4"]
        assert list(sorted_repository_data.keys())[0] == "repository_11"

    if data_index == 8:
        assert list(sorted_team_data.keys()) == ["team1", "team2", "team3", "team4"]

    processed_data.clear()
    sorted_team_data.clear()
    sorted_repository_data.clear()
