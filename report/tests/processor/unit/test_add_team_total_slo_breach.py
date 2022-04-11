# -*- coding: utf-8 -*-


def test_add_team_total_slo_breach(processor, scene_index, scene_data):
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

    check_team_total_slo_breach(scene_index=scene_index, teams=processor.teams)

    processor.clear()


def check_team_total_slo_breach(scene_index, teams):

    """
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """
    team1_slo_breach_repositories = teams["team1"]["total"]["slo_breach"][
        "repositories"
    ]
    team2_slo_breach_repositories = teams["team2"]["total"]["slo_breach"][
        "repositories"
    ]
    team3_slo_breach_repositories = teams["team3"]["total"]["slo_breach"][
        "repositories"
    ]
    team4_slo_breach_repositories = teams["team4"]["total"]["slo_breach"][
        "repositories"
    ]

    team1_slo_breach_sum = sum(
        value for value in teams["team1"]["total"]["slo_breach"]["severities"].values()
    )

    team2_slo_breach_sum = sum(
        value for value in teams["team2"]["total"]["slo_breach"]["severities"].values()
    )

    team3_slo_breach_sum = sum(
        value for value in teams["team3"]["total"]["slo_breach"]["severities"].values()
    )

    team4_slo_breach_sum = sum(
        value for value in teams["team4"]["total"]["slo_breach"]["severities"].values()
    )

    if scene_index == 1:
        assert team1_slo_breach_sum == 2
        assert team2_slo_breach_sum == 4
        assert team3_slo_breach_sum == 0
        assert team4_slo_breach_sum == 0

        assert team1_slo_breach_repositories == 2
        assert team2_slo_breach_repositories == 4
        assert team3_slo_breach_repositories == 0
        assert team4_slo_breach_repositories == 0

    if scene_index == 2:
        assert team1_slo_breach_sum == 2
        assert team2_slo_breach_sum == 4
        assert team3_slo_breach_sum == 0
        assert team4_slo_breach_sum == 0

        assert team1_slo_breach_repositories == 2
        assert team2_slo_breach_repositories == 4
        assert team3_slo_breach_repositories == 0
        assert team4_slo_breach_repositories == 0

    if scene_index == 8:
        assert team1_slo_breach_sum == 0
        assert team2_slo_breach_sum == 0
        assert team3_slo_breach_sum == 0
        assert team4_slo_breach_sum == 0

        assert team1_slo_breach_repositories == 0
        assert team2_slo_breach_repositories == 0
        assert team3_slo_breach_repositories == 0
        assert team4_slo_breach_repositories == 0
