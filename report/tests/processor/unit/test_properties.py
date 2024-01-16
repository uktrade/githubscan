# -*- coding: utf-8 -*-

from unit import (
    check_add_enterprise_users,
    check_orphan_repositorie,
    check_repositores,
    check_skip_scan_repositories,
    check_token_has_no_access,
    check_vulnerable_repositories,
)


def test_processed_data_empty_before_loading(processor):
    assert processor.processed_data["enterprise_users"] == {}
    assert processor.processed_data["repositories"] == {}
    assert processor.processed_data["teams"] == {}
    assert processor.processed_data["skip_scan_repositories"] == {}
    assert processor.processed_data["orphan_repositories"] == {}
    assert processor.processed_data["vulnerable_repositories"] == []
    assert processor.processed_data["token_has_no_access"] == []
    assert processor.processed_data["severity_status"] == ""


def test_report_properties_empty_before_loading(processor):
    assert processor.enterprise_users == {}
    assert processor.repositories == {}
    assert processor.teams == {}
    assert processor.skip_scan_repositories == {}
    assert processor.orphan_repositories == {}
    assert processor.vulnerable_repositories == []
    assert processor.token_has_no_access == []


def test_enterprise_user_property(processor, scene_index, scene_data):
    processor.load_data_from_dict = scene_data

    processor.add_enterprise_users()

    check_add_enterprise_users(enterprise_users=processor.enterprise_users)


def test_repositories_property(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()

    check_repositores(repositories=processor.repositories)

    processor.clear()


def test_vulnerable_repositories_property(processor, scene_index, scene_data):
    """
    test it for all scenarios
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()

    check_vulnerable_repositories(
        scene_index=scene_index,
        vulnerable_repositories=processor.vulnerable_repositories,
    )

    processor.clear()


def test_skip_scan_repositories_property(processor, scene_index, scene_data):
    """
    test it for all scenarios
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_skip_scan_repositories()

    check_skip_scan_repositories(
        repositories=processor.repositories,
        skip_scan_repositories_list=processor.skip_scan_repositories["list"],
    )

    processor.clear()


def test_token_has_no_access_property(processor, scene_index, scene_data):
    """
    test it for all scenarios
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """
    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_teams_and_team_repositories()
    processor.add_token_has_no_access()

    check_token_has_no_access(token_has_no_access=processor.token_has_no_access)

    processor.clear()


def test_orphan_repositories_property(processor, scene_index, scene_data):
    """
    test it for all scenarios
    refer to mock_test_data -> generate_scenarios, for how we work out these numbers
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_teams_and_team_repositories()
    processor.add_orphan_repositories()

    check_orphan_repositorie(
        orphan_repositories_list=processor.orphan_repositories["list"]
    )

    processor.clear()


def test_exception_orphan_repositories_setter_property(processor, caplog):
    try:
        processor.orphan_repositories = "this,is,bad"
        assert False
    except TypeError:
        assert "repository_list expected to be list type but is str" in caplog.messages
        assert True


def test_orphan_repositories_setter_property(processor):
    my_list = ["one", "two", "three"]
    processor.orphan_repositories = my_list

    assert processor.orphan_repositories["list"] == my_list

    processor.clear()


def test_exception_token_has_no_access_setter_property(processor, caplog):
    try:
        processor.token_has_no_access = "this,is,bad"
        assert False
    except TypeError:
        assert "repository_list expected to be list type but is str" in caplog.messages
        assert True


def test_token_has_no_access_setter_property(processor):
    my_list = sorted(["one", "two", "three"])
    processor.token_has_no_access = my_list

    assert sorted(processor.token_has_no_access) == my_list

    processor.clear()
