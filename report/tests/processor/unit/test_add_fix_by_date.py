# -*- coding: utf-8 -*-
def test_add_fix_by_date(processor, scene_index, scene_data):
    """test it for all scenarios"""
    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_fix_by_date()

    check_fix_by_date(repositories=processor.repositories)

    processor.clear()


def check_fix_by_date(repositories):
    for repository in repositories.values():
        for alert in repository["alerts"]:
            assert alert["fix_by"] == alert["test_expected_data"]["fix_by"]
