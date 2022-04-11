# -*- coding: utf-8 -*-
from config.severities import EFFECTIVE_SEVERITY


def test_add_organization_totals_severities(processor, scene_index, scene_data):
    """test it for all scenarios"""

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_skip_scan_repositories()
    processor.add_repository_totals()
    processor.add_organization_totals()

    check_organization_totals_severities(
        scene_index=scene_index,
        severities=processor.processed_data["total"]["severities"],
    )

    processor.clear()


def check_organization_totals_severities(scene_index, severities):
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
        assert original_sum == 11
        assert effective_sum == 11

    if scene_index == 2 or scene_index == 5:
        assert original_sum == 8
        assert effective_sum == 8

    if scene_index == 3:
        assert original_sum == 6
        assert effective_sum == 6

    if scene_index == 4 or scene_index == 7:
        assert original_sum == 3
        assert effective_sum == 3

    if scene_index == 6:
        assert original_sum == 5
        assert effective_sum == 5

    if scene_index == 8:
        assert original_sum == 0
        assert effective_sum == 0
