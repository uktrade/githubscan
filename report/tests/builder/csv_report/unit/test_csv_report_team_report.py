# -*- coding: utf-8 -*-
def test_csv_report_with_team_data(
    build_csv_report, report_reader, data_index, processed_data
):
    """
    Could be improved to check csv content and ensure it matches the expected data
    """
    report_reader.load_data_from_dict = processed_data

    for team in report_reader.teams.keys():
        crated_csv = build_csv_report.team_report(
            team=team, report_reader=report_reader
        )
        assert crated_csv.exists()
        crated_csv.unlink()
