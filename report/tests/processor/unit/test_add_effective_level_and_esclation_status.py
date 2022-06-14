# -*- coding: utf-8 -*-
def test_add_effective_level_and_escalation_status(processor, scene_index, scene_data):

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()

    check_effective_level_and_escalation_status(repositories=processor.repositories)

    processor.clear()


def check_effective_level_and_escalation_status(repositories):
    for repository in repositories.values():
        for alert in repository["alerts"]:
            assert (
                alert["effective_level"]
                == alert["test_expected_data"]["effective_level"]
            )
