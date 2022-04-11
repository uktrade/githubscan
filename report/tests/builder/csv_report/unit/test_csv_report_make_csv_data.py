# -*- coding: utf-8 -*-
def test_csv_report_make_csv_data_in_correct_data_tye(build_csv_report, caplog):
    try:
        repositories_list = "this is string"
        build_csv_report._make_csv_data_(repositories_list=repositories_list)
        assert False
    except TypeError:
        assert (
            "repositories_list expected to be list type but is str" in caplog.messages
        )
        assert True


def test_csv_report_with_organization_data(
    build_csv_report, report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data

    repositories_list = report_reader.reportable_organization_repositories_list

    csv_data = build_csv_report._make_csv_data_(repositories_list=repositories_list)

    assert len(csv_data) == len(repositories_list) + 1

    report_reader.clear()

    build_csv_report.clear()


def test_csv_report_with_team_data(
    build_csv_report, report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data

    for team in report_reader.teams.keys():
        repositories_list = report_reader.reportable_team_repositories_list(team=team)

        csv_data = build_csv_report._make_csv_data_(repositories_list=repositories_list)

        assert len(csv_data) == len(repositories_list) + 1

        build_csv_report.clear()

    report_reader.clear()
