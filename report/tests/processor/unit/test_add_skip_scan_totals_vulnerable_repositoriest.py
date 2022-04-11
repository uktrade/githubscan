# -*- coding: utf-8 -*-
def test_add_skip_scan_totals_vulnerable_repositoriest(
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

    check_skip_scan_totals_vulnerable_repositoriest(
        scene_index=scene_index,
        vulnerable_repositories_count=processor.skip_scan_repositories["total"][
            "repositories"
        ],
    )

    processor.clear()


def check_skip_scan_totals_vulnerable_repositoriest(
    scene_index, vulnerable_repositories_count
):

    if scene_index == 1:
        assert vulnerable_repositories_count == 3

    if scene_index == 2 or scene_index == 3 or scene_index == 5:
        assert vulnerable_repositories_count == 2

    if scene_index == 4 or scene_index == 6 or scene_index == 7:
        assert vulnerable_repositories_count == 1

    if scene_index == 8:
        assert vulnerable_repositories_count == 0
