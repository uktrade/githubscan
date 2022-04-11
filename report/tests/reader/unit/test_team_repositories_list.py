# -*- coding: utf-8 -*-
def test_team_repositories_list(report_reader, data_index, processed_data):

    report_reader.load_data_from_dict = processed_data

    team1_repository_list = report_reader.team_repositories_list(team="team1")
    team2_repository_list = report_reader.team_repositories_list(team="team2")
    team3_repository_list = report_reader.team_repositories_list(team="team3")
    team4_repository_list = report_reader.team_repositories_list(team="team4")

    assert len(team1_repository_list) == 2
    assert len(team2_repository_list) == 4
    assert len(team3_repository_list) == 2
    assert len(team4_repository_list) == 1

    report_reader.clear()
