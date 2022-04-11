# -*- coding: utf-8 -*-
def test_add_orphan_repositories(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_teams_and_team_repositories()
    processor.add_orphan_repositories()

    check_orphan_repositorie(
        orphan_repositories_list=processor.orphan_repositories["list"]
    )

    processor.clear()


def check_orphan_repositorie(orphan_repositories_list):
    """
    for all scene count of orphan repositorie is same
    so we do not need if scene_index == 1 , 2 etc
    """
    assert len(orphan_repositories_list) == 3
