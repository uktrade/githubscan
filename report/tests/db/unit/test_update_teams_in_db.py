# -*- coding: utf-8 -*-
from report.db import update_teams_in_db
from report.models import Team


def test_update_teams_in_db_with_wrong_data_type(db, caplog):
    try:
        teams = "test-t1"
        update_teams_in_db(github_teams=teams)
        assert False
    except TypeError:
        assert "github_teams expected to be list but it is a str"
        assert True


def test_update_teams_in_db_with_data(db):
    teams = sorted(["test-t1", "test-t2", "test-t3"])
    update_teams_in_db(github_teams=teams)

    teams_in_db = sorted(list(Team.objects.all().values_list("name", flat=True)))

    assert teams == teams_in_db


def test_update_teams_in_db_for_no_repeat(db):
    teams_1 = sorted(["test-t1", "test-t2", "test-t3"])
    update_teams_in_db(github_teams=teams_1)

    teams_2 = sorted(["test-t2", "test-t3", "test-t4"])
    update_teams_in_db(github_teams=teams_2)

    """
    Get unique values from merged list just as epxected from db
    """
    teams = sorted(list(set(teams_1 + teams_2)))

    teams_in_db = sorted(list(Team.objects.all().values_list("name", flat=True)))

    assert teams == teams_in_db
