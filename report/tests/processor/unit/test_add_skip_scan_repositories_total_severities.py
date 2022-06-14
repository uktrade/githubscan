# -*- coding: utf-8 -*-
def test_add_skip_scan_repositories_total_severities(
    processor, scene_index, scene_data
):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_teams_and_team_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_repository_totals()
    processor.add_skip_scan_repositories()
    processor.add_skip_scan_repositories_totals()

    check_skip_scan_repositories_total_severitie(
        scene_index=scene_index,
        severities=processor.skip_scan_repositories["total"]["severities"],
    )

    processor.clear()


def check_skip_scan_repositories_total_severitie(scene_index, severities):

    original_sum = sum(value for value in severities["original"].values())

    effective_sum = sum(value for value in severities["effective"].values())

    assert original_sum == effective_sum

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
