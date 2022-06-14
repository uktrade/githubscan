# -*- coding: utf-8 -*-
from config.severities import SEVERITY_STATUS


def test_add_orphan_repositories_severity_status(processor, scene_index, scene_data):
    """test it for all scenarios"""

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_teams_and_team_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_repository_severity_status()
    processor.add_orphan_repositories()
    processor.add_orphan_repositories_severity_status()

    check_orphan_repositories_severity_status(
        scene_index=scene_index,
        severity_status=processor.orphan_repositories["severity_status"],
    )

    processor.clear()


def check_orphan_repositories_severity_status(scene_index, severity_status):

    if scene_index == 1 or scene_index == 2 or scene_index == 3 or scene_index == 4:
        assert severity_status == SEVERITY_STATUS.RED.name

    if scene_index == 5 or scene_index == 6:
        assert severity_status == SEVERITY_STATUS.AMBER.name

    if scene_index == 7:
        assert severity_status == SEVERITY_STATUS.GREEN.name

    if scene_index == 8:
        assert severity_status == SEVERITY_STATUS.CLEAN.name
