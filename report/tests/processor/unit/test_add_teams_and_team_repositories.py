# -*- coding: utf-8 -*-


def test_add_teams_and_team_repositories(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_teams_and_team_repositories()

    check_teams_and_team_repositories(processor.teams)

    processor.clear()


def check_teams_and_team_repositories(teams):
    assert 4 == len(teams.keys())
    assert 4 == len(teams["team1"]["repositories"])
    assert 6 == len(teams["team2"]["repositories"])
    assert 4 == len(teams["team3"]["repositories"])
    assert 2 == len(teams["team4"]["repositories"])
