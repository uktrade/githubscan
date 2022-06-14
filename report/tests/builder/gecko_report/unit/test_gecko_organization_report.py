# -*- coding: utf-8 -*-
def test_organizaition(build_gecko_report, report_reader, data_index, processed_data):

    report_reader.load_data_from_dict = processed_data

    max_report_repos = 2

    build_gecko_report.max_report_repositories = max_report_repos

    build_gecko_report.organizaition(report_reader=report_reader)

    report = build_gecko_report.organization_report

    assert len(report) == max_report_repos

    build_gecko_report.clear()
    processed_data.clear()
