# -*- coding: utf-8 -*-
from report.db import get_teams_from_db
from report.models import Team


def test_get_teams_from_db(db):
    Team(name="test-t1", reporting_enabled=False).save()
    Team(name="test-t2", reporting_enabled=True).save()

    teams = get_teams_from_db()

    sorted_teams = sorted(list(teams.values_list("name", flat=True)))

    assert sorted_teams == ["test-t1", "test-t2"]

    assert teams.get(name="test-t1").reporting_enabled == False
    assert teams.get(name="test-t2").reporting_enabled == True
