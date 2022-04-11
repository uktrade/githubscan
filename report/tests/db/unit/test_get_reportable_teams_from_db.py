# -*- coding: utf-8 -*-
from report.db import get_reportable_teams_from_db
from report.models import Team


def test_get_reportable_teams_from_db_with_one_disabled(db):
    Team(name="test-t1", reporting_enabled=False).save()
    Team(name="test-t2", reporting_enabled=True).save()

    teams_set = set(get_reportable_teams_from_db().values_list("name", flat=True))

    assert "test-t2" in teams_set
    assert "test-t1" not in teams_set


def test_get_reportable_teams_from_db_with_default_reporting(db):
    Team(name="test-t1").save()
    Team(name="test-t2").save()

    teams = get_reportable_teams_from_db()

    sorted_teams = sorted(list(teams.values_list("name", flat=True)))

    assert sorted_teams == ["test-t1", "test-t2"]

    assert teams.get(name="test-t1").reporting_enabled == True
    assert teams.get(name="test-t2").reporting_enabled == True
