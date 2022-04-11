# -*- coding: utf-8 -*-
import re


def test_add_repository_teams(processor, scene_index, scene_data):
    """test it for all scenarios"""

    processor.load_data_from_dict = scene_data

    processor.add_repositories()
    processor.add_repository_teams()

    check_add_repository_teams(repositories=processor.repositories)

    processor.clear()


def check_add_repository_teams(repositories):
    for repository_name in repositories.keys():
        if re.match("repository_0[1-3]$", repository_name):
            assert repositories[repository_name]["teams"] == ["team1"]

        if re.match("repository_(0[5-6]|9)$|repository_10", repository_name):
            assert repositories[repository_name]["teams"] == ["team2"]

        if re.match("repository_1[1-3]$", repository_name):
            assert repositories[repository_name]["teams"] == ["team3"]

        if re.match("repository_15$", repository_name):
            assert repositories[repository_name]["teams"] == ["team4"]
