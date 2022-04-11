# -*- coding: utf-8 -*-
def test_add_vulnerable_repositories(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()

    check_vulnerable_repositories(
        scene_index=scene_index,
        vulnerable_repositories=processor.vulnerable_repositories,
    )

    processor.clear()


def check_vulnerable_repositories(scene_index, vulnerable_repositories):

    if scene_index == 1:
        assert 14 == len(vulnerable_repositories)

    if scene_index == (2 or 5):
        assert 10 == len(vulnerable_repositories)

    if scene_index == 3:
        assert 8 == len(vulnerable_repositories)

    if scene_index == 4 or scene_index == 7:
        assert 4 == len(vulnerable_repositories)

    if scene_index == 6:
        assert 6 == len(vulnerable_repositories)

    if scene_index == 8:
        assert 0 == len(vulnerable_repositories)
