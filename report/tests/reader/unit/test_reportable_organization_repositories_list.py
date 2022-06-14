# -*- coding: utf-8 -*-
def test_reportable_organization_repositories_list(
    report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data

    repository_list = report_reader.reportable_organization_repositories_list

    if data_index == 1:
        assert len(repository_list) == 11

    if data_index == 2 or data_index == 5:
        assert len(repository_list) == 8

    if data_index == 3:
        assert len(repository_list) == 6

    if data_index == 4 or data_index == 7:
        assert len(repository_list) == 3

    if data_index == 6:
        assert len(repository_list) == 5

    if data_index == 8:
        assert len(repository_list) == 0

    report_reader.clear()
