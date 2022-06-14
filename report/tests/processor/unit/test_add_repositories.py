# -*- coding: utf-8 -*-
def test_add_repositories(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """
    processor.load_data_from_dict = scene_data
    processor.add_repositories()

    check_repositores(repositories=processor.repositories)

    processor.clear()


def check_repositores(repositories):
    assert 15 == len(repositories.keys())
