# -*- coding: utf-8 -*-
import re


def test_add_repository_totals(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_repository_totals()

    check_repository_totals(
        scene_index=scene_index, repositories=processor.repositories
    )

    processor.clear()


def check_repository_totals(scene_index, repositories):
    """
    ensure sum of orignal severity is same as sum of effective severity
    """

    for repository in repositories.values():
        slo_breach_repositories = 0
        original_sum = sum(
            value for value in repository["total"]["severities"]["original"].values()
        )

        effective_sum = sum(
            value for value in repository["total"]["severities"]["effective"].values()
        )

        assert original_sum == effective_sum

        slo_breach_sum = sum(
            value for value in repository["total"]["slo_breach"]["severities"].values()
        )

        slo_breach_repositories = repository["total"]["slo_breach"]["repositories"]

        if scene_index == 1:
            if re.match("repository_(0[1-9]$|10$)", repository["name"]):
                assert slo_breach_sum == 1
                assert slo_breach_repositories == 1
            else:
                assert slo_breach_sum == 0
                assert slo_breach_repositories == 0

            if re.match("repository_(0[1-9]$|1[0-4]$)", repository["name"]):
                assert repository["total"]["repositories"] == 1
                assert original_sum == 1
                assert effective_sum == 1
            else:
                assert repository["total"]["repositories"] == 0
                assert original_sum == 0
                assert effective_sum == 0

        if scene_index == 2:
            if re.match("repository_(0[1-9]$|10$)", repository["name"]):
                assert repository["total"]["repositories"] == 1
                assert original_sum == 1
                assert effective_sum == 1
                assert slo_breach_sum == 1
                assert slo_breach_repositories == 1
            else:
                assert repository["total"]["repositories"] == 0
                assert original_sum == 0
                assert effective_sum == 0
                assert slo_breach_sum == 0
                assert slo_breach_repositories == 0

        if scene_index == 8:
            assert repository["total"]["repositories"] == 0
            assert original_sum == 0
            assert effective_sum == 0
            assert slo_breach_sum == 0
            assert slo_breach_repositories == 0
