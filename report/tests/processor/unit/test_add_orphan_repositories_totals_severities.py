# -*- coding: utf-8 -*-
from config.severities import EFFECTIVE_SEVERITY


def test_add_orphan_repositories_totals_severities(processor, scene_index, scene_data):
    """test it for all scenarios"""

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_teams_and_team_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_repository_totals()
    processor.add_orphan_repositories()
    processor.add_orphan_repositories_totals()

    check_orphan_repositories_totals_severities(
        scene_index=scene_index,
        severities=processor.orphan_repositories["total"]["severities"],
    )

    processor.clear()


def check_orphan_repositories_totals_severities(scene_index, severities):
    """
    ensure sum of orignal severity is same as sum of effective severity
    """
    original_sum = sum(value for value in severities["original"].values())

    effective_sum = sum(value for value in severities["effective"].values())

    assert EFFECTIVE_SEVERITY.CRITICAL_BREACH.name not in severities["original"]

    assert original_sum == effective_sum

    """
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """
    if scene_index == 1:
        assert original_sum == 3
        assert effective_sum == 3

    if scene_index == 2 or scene_index == 3 or scene_index == 5:
        assert original_sum == 2
        assert effective_sum == 2

    if scene_index == 4 or scene_index == 6 or scene_index == 7:
        assert original_sum == 1
        assert effective_sum == 1

    if scene_index == 8:
        assert original_sum == 0
        assert effective_sum == 0
