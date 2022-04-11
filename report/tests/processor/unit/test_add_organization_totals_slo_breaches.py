# -*- coding: utf-8 -*-
def test_add_organization_totals_slo_breaches(processor, scene_index, scene_data):
    """test it for all scenarios"""
    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_skip_scan_repositories()
    processor.add_repository_totals()
    processor.add_organization_totals()

    check_organization_totals_slo_breaches(
        scene_index=scene_index,
        slo_breach=processor.processed_data["total"]["slo_breach"],
    )

    processor.clear()


def check_organization_totals_slo_breaches(scene_index, slo_breach):

    slo_breach_sum = sum(value for value in slo_breach["severities"].values())
    slo_breach_repositories = slo_breach["repositories"]

    """
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """
    if scene_index == 1 or scene_index == 2:
        assert slo_breach_sum == 8
        assert slo_breach_repositories == 8

    if scene_index == 3 or scene_index == 4:
        assert slo_breach_sum == 3
        assert slo_breach_repositories == 3

    if scene_index == 5 or scene_index == 6:
        assert slo_breach_sum == 5
        assert slo_breach_repositories == 5

    if scene_index == 7 or scene_index == 8:
        assert slo_breach_sum == 0
        assert slo_breach_repositories == 0
