# -*- coding: utf-8 -*-
def test_add_team_totals_vulnerable_repositories(processor, scene_index, scene_data):
    """
    test it for all scenarios
    refer to mock_test_data generate_scenarios() to know which team is expected to have which status
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_teams_and_team_repositories()
    processor.add_token_has_no_access()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_repository_totals()
    processor.add_skip_scan_repositories()
    processor.add_team_totals()

    check_team_totals_vulnerable_repositories(
        scene_index=scene_index, teams=processor.teams
    )

    processor.clear()


def check_team_totals_vulnerable_repositories(scene_index, teams):

    """
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """
    if scene_index == 1:
        assert teams["team1"]["total"]["repositories"] == 2
        assert teams["team2"]["total"]["repositories"] == 4
        assert teams["team3"]["total"]["repositories"] == 2
        assert teams["team4"]["total"]["repositories"] == 0

    if scene_index == 2:
        assert teams["team1"]["total"]["repositories"] == 2
        assert teams["team2"]["total"]["repositories"] == 4
        assert teams["team3"]["total"]["repositories"] == 0
        assert teams["team4"]["total"]["repositories"] == 0

    if scene_index == 8:
        assert teams["team1"]["total"]["repositories"] == 0
        assert teams["team2"]["total"]["repositories"] == 0
        assert teams["team3"]["total"]["repositories"] == 0
        assert teams["team4"]["total"]["repositories"] == 0
