# -*- coding: utf-8 -*-
from report.helper.functions import sort_list_by_total


def test_sort_list_by_total(data_index, processed_data):

    repositories_list = [value for value in processed_data["repositories"].values()]

    sorted_repositories_list = sort_list_by_total(data=repositories_list)

    if data_index == 1 or data_index == 2 or data_index == 3 or data_index == 4:
        assert sorted_repositories_list[0]["name"] == "repository_01"

    if data_index == 5 or data_index == 6:
        assert sorted_repositories_list[0]["name"] == "repository_05"

    if data_index == 7:
        assert sorted_repositories_list[0]["name"] == "repository_11"

    processed_data.clear()
    repositories_list.clear()
