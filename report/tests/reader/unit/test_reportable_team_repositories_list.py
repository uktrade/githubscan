# -*- coding: utf-8 -*-
def test_reportable_team_repositories_list(report_reader, data_index, processed_data):

    report_reader.load_data_from_dict = processed_data

    team1_repositories_list = report_reader.reportable_team_repositories_list(
        team="team1"
    )
    team2_repositories_list = report_reader.reportable_team_repositories_list(
        team="team2"
    )
    team3_repositories_list = report_reader.reportable_team_repositories_list(
        team="team3"
    )
    team4_repositories_list = report_reader.reportable_team_repositories_list(
        team="team4"
    )

    if data_index == 1:
        assert len(team1_repositories_list) == 2
        assert len(team2_repositories_list) == 4
        assert len(team3_repositories_list) == 2
        assert len(team4_repositories_list) == 0

    if data_index == 2:
        assert len(team1_repositories_list) == 2
        assert len(team2_repositories_list) == 4
        assert len(team3_repositories_list) == 0
        assert len(team4_repositories_list) == 0

    if data_index == 3:
        assert len(team1_repositories_list) == 2
        assert len(team2_repositories_list) == 0
        assert len(team3_repositories_list) == 2
        assert len(team4_repositories_list) == 0

    if data_index == 4:
        assert len(team1_repositories_list) == 2
        assert len(team2_repositories_list) == 0
        assert len(team3_repositories_list) == 0
        assert len(team4_repositories_list) == 0

    if data_index == 5:
        assert len(team1_repositories_list) == 0
        assert len(team2_repositories_list) == 4
        assert len(team3_repositories_list) == 2
        assert len(team4_repositories_list) == 0

    if data_index == 6:
        assert len(team1_repositories_list) == 0
        assert len(team2_repositories_list) == 4
        assert len(team3_repositories_list) == 0
        assert len(team4_repositories_list) == 0

    if data_index == 7:
        assert len(team1_repositories_list) == 0
        assert len(team2_repositories_list) == 0
        assert len(team3_repositories_list) == 2
        assert len(team4_repositories_list) == 0

    if data_index == 8:
        assert len(team1_repositories_list) == 0
        assert len(team2_repositories_list) == 0
        assert len(team3_repositories_list) == 0
        assert len(team4_repositories_list) == 0

    report_reader.clear()
