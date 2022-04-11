# -*- coding: utf-8 -*-
def test_organization_repositories_list(report_reader, data_index, processed_data):

    report_reader.load_data_from_dict = processed_data

    repository_list = report_reader.organization_repositories_list

    assert len(repository_list) == 12

    report_reader.clear()
