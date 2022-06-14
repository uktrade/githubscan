# -*- coding: utf-8 -*-
def test_add_organization_totals_vulnerable_repositories(
    processor, scene_index, scene_data
):
    """test it for all scenarios"""
    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_skip_scan_repositories()
    processor.add_repository_totals()
    processor.add_organization_totals()

    check_organization_totals_vulnerable_repositories(
        scene_index=scene_index,
        vulnerable_repositories=processor.processed_data["total"]["repositories"],
    )

    processor.clear()


def check_organization_totals_vulnerable_repositories(
    scene_index, vulnerable_repositories
):

    """
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """

    if scene_index == 1:
        assert vulnerable_repositories == 11

    if scene_index == 2 or scene_index == 5:
        assert vulnerable_repositories == 8

    if scene_index == 3:
        assert vulnerable_repositories == 6

    if scene_index == 4 or scene_index == 7:
        assert vulnerable_repositories == 3

    if scene_index == 6:
        assert vulnerable_repositories == 5

    if scene_index == 8:
        assert vulnerable_repositories == 0
