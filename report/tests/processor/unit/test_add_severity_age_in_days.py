# -*- coding: utf-8 -*-
def test_add_severity_age_in_days(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_severity_age_in_days()

    check_severity_age_in_days(repositories=processor.repositories)

    processor.clear()


def check_severity_age_in_days(repositories):
    for repository in repositories.values():
        for alert in repository["alerts"]:
            assert (
                alert["age_in_business_days"]
                == alert["test_expected_data"]["age_in_business_days"]
            )

            assert (
                alert["age_in_calendar_days"]
                == alert["test_expected_data"]["age_in_calendar_days"]
            )
