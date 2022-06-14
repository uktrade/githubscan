# -*- coding: utf-8 -*-
def test_add_skip_scan_repositories_slo_breach_totals(
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

    check_skip_scan_repositories_slo_breach_totals(
        scene_index=scene_index,
        slo_breach=processor.skip_scan_repositories["total"]["slo_breach"],
    )

    processor.clear()


def check_skip_scan_repositories_slo_breach_totals(scene_index, slo_breach):

    slo_breach_sum = sum(value for value in slo_breach["severities"].values())
    slo_breach_repositories = slo_breach["repositories"]

    if scene_index == 1 or scene_index == 2:
        assert slo_breach_sum == 2
        assert slo_breach_repositories == 2

    if scene_index == 3 or scene_index == 4 or scene_index == 5 or scene_index == 6:
        assert slo_breach_sum == 1
        assert slo_breach_repositories == 1

    if scene_index == 7 or scene_index == 8:
        assert slo_breach_sum == 0
        assert slo_breach_repositories == 0
