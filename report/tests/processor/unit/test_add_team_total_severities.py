# -*- coding: utf-8 -*-
from config.severities import EFFECTIVE_SEVERITY


def test_add_team_total_severities(processor, scene_index, scene_data):
    """
    test it for all scenarios
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

    check_team_total_severities(scene_index=scene_index, teams=processor.teams)

    processor.clear()


def check_team_total_severities(scene_index, teams):

    for team_info in teams.values():

        team_total = team_info["total"]

        assert (
            EFFECTIVE_SEVERITY.CRITICAL_BREACH.name
            not in team_total["severities"]["original"]
        )

        original_sum = sum(
            value for value in team_info["total"]["severities"]["original"].values()
        )

        effective_sum = sum(
            value for value in team_info["total"]["severities"]["effective"].values()
        )

        assert original_sum == effective_sum

    team1_severities_sum = sum(
        value for value in teams["team1"]["total"]["severities"]["original"].values()
    )

    team2_severities_sum = sum(
        value for value in teams["team2"]["total"]["severities"]["original"].values()
    )

    team3_severities_sum = sum(
        value for value in teams["team3"]["total"]["severities"]["original"].values()
    )

    team4_severities_sum = sum(
        value for value in teams["team4"]["total"]["severities"]["original"].values()
    )

    """
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """

    if scene_index == 1:
        assert team1_severities_sum == 2
        assert team2_severities_sum == 4
        assert team3_severities_sum == 2
        assert team4_severities_sum == 0

    if scene_index == 2:
        assert team1_severities_sum == 2
        assert team2_severities_sum == 4
        assert team3_severities_sum == 0
        assert team4_severities_sum == 0

    if scene_index == 8:
        assert team1_severities_sum == 0
        assert team2_severities_sum == 0
        assert team3_severities_sum == 0
        assert team4_severities_sum == 0
