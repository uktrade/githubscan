# -*- coding: utf-8 -*-
from pathlib import Path

test_root_path = Path(__file__).parent


def test_csv_report_write_csv_file_in_correct_path_type(build_csv_report, caplog):
    try:
        path = "this is string"
        build_csv_report._write_csv_file_(path=path, csv_content=[])
        assert False
    except TypeError:
        assert "path expected to be PosixPath type but is str" in caplog.messages
        assert True


def test_csv_report_write_csv_file_in_correct_csv_content_type(
    build_csv_report, caplog
):
    global test_root_path
    try:
        path = test_root_path
        build_csv_report._write_csv_file_(path=test_root_path, csv_content="string")
        assert False
    except TypeError:
        assert "csv_content expected to be list type but is str" in caplog.messages
        assert True


def test_csv_report_write_with_organization_data(
    build_csv_report, report_reader, data_index, processed_data
):

    global test_root_path

    file_path = Path.joinpath(test_root_path, "test_org_report.csv")

    report_reader.load_data_from_dict = processed_data

    repositories_list = report_reader.reportable_organization_repositories_list

    csv_data = build_csv_report._make_csv_data_(repositories_list=repositories_list)

    assert file_path.exists() == False

    build_csv_report._write_csv_file_(path=file_path, csv_content=csv_data)

    assert file_path.exists()

    file_path.unlink()

    report_reader.clear()

    build_csv_report.clear()


def test_csv_report_write_with_team_data(
    build_csv_report, report_reader, data_index, processed_data
):
    global test_root_path

    report_reader.load_data_from_dict = processed_data

    for team in report_reader.teams.keys():

        repositories_list = report_reader.reportable_team_repositories_list(team=team)

        csv_data = build_csv_report._make_csv_data_(repositories_list=repositories_list)

        file_path = Path.joinpath(test_root_path, f"{team}.csv")

        assert file_path.exists() == False

        build_csv_report._write_csv_file_(path=file_path, csv_content=csv_data)

        assert file_path.exists()

        file_path.unlink()

        build_csv_report.clear()

    report_reader.clear()
