# -*- coding: utf-8 -*-
def test_team_report(build_gecko_report, report_reader, data_index, processed_data):

    report_reader.load_data_from_dict = processed_data

    max_report_repos = 2

    build_gecko_report.max_report_repositories = max_report_repos

    build_gecko_report.teams(report_reader=report_reader)

    report = build_gecko_report.teams_report

    assert len(report["team1"]) == max_report_repos
    assert len(report["team2"]) == max_report_repos
    assert len(report["team3"]) == max_report_repos
    assert len(report["team4"]) == 1

    """
    What we are checking here is what would be first based on sorting
    for given scene index
    refer to mock_test_data.py for more information
    """

    assert report["team1"][0]["repository"] == "repository_01"
    assert report["team2"][0]["repository"] == "repository_05"
    assert report["team3"][0]["repository"] == "repository_11"
    assert report["team4"][0]["repository"] == "repository_15"

    build_gecko_report.clear()
    processed_data.clear()
