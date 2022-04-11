# -*- coding: utf-8 -*-
import re


def test_add_token_has_no_access(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_teams_and_team_repositories()
    processor.add_token_has_no_access()

    check_token_has_no_access(token_has_no_access=processor.token_has_no_access)

    processor.clear()


def check_token_has_no_access(token_has_no_access):
    """
    ensure repository names are matching pattern for
    token_has_no_access repositories i.e. "repository_[1-9][0-9][0-9]"
    """
    for repository_name in token_has_no_access:
        assert re.match("repository_[1-9][0-9][0-9]", repository_name)

    assert 4 == len(token_has_no_access)
