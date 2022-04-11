# -*- coding: utf-8 -*-
from config.severities import SEVERITY_STATUS
from collections import Counter


def test_add_repository_severity_status(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_repository_severity_status()

    check_repository_severity_status(
        scene_index=scene_index, repositories=processor.repositories
    )

    processor.clear()


def check_repository_severity_status(scene_index, repositories):
    counter = Counter()

    for repository in repositories.values():
        counter[repository["severity_status"]] += 1

    if scene_index == 1:
        assert counter[SEVERITY_STATUS.RED.name] == 4
        assert counter[SEVERITY_STATUS.AMBER.name] == 6
        assert counter[SEVERITY_STATUS.GREEN.name] == 4
        assert counter[SEVERITY_STATUS.CLEAN.name] == 1

    if scene_index == 2:
        assert counter[SEVERITY_STATUS.RED.name] == 4
        assert counter[SEVERITY_STATUS.AMBER.name] == 6
        assert counter[SEVERITY_STATUS.GREEN.name] == 0
        assert counter[SEVERITY_STATUS.CLEAN.name] == 1 + 4

    if scene_index == 3:
        assert counter[SEVERITY_STATUS.RED.name] == 4
        assert counter[SEVERITY_STATUS.AMBER.name] == 0
        assert counter[SEVERITY_STATUS.GREEN.name] == 4
        assert counter[SEVERITY_STATUS.CLEAN.name] == 1 + 6

    if scene_index == 4:
        assert counter[SEVERITY_STATUS.RED.name] == 4
        assert counter[SEVERITY_STATUS.AMBER.name] == 0
        assert counter[SEVERITY_STATUS.GREEN.name] == 0
        assert counter[SEVERITY_STATUS.CLEAN.name] == 1 + 4 + 6

    if scene_index == 5:
        assert counter[SEVERITY_STATUS.RED.name] == 0
        assert counter[SEVERITY_STATUS.AMBER.name] == 6
        assert counter[SEVERITY_STATUS.GREEN.name] == 4
        assert counter[SEVERITY_STATUS.CLEAN.name] == 1 + 4

    if scene_index == 6:
        assert counter[SEVERITY_STATUS.RED.name] == 0
        assert counter[SEVERITY_STATUS.AMBER.name] == 6
        assert counter[SEVERITY_STATUS.GREEN.name] == 0
        assert counter[SEVERITY_STATUS.CLEAN.name] == 1 + 4 + 4

    if scene_index == 7:
        assert counter[SEVERITY_STATUS.RED.name] == 0
        assert counter[SEVERITY_STATUS.AMBER.name] == 0
        assert counter[SEVERITY_STATUS.GREEN.name] == 4
        assert counter[SEVERITY_STATUS.CLEAN.name] == 1 + 4 + 6

    if scene_index == 8:
        assert counter[SEVERITY_STATUS.RED.name] == 0
        assert counter[SEVERITY_STATUS.AMBER.name] == 0
        assert counter[SEVERITY_STATUS.GREEN.name] == 0
        assert counter[SEVERITY_STATUS.CLEAN.name] == 1 + 4 + 6 + 4
