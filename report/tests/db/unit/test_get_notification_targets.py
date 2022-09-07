# -*- coding: utf-8 -*-
from report.db import get_teams_from_db, get_team_notification_targets
from report.models import Team, TeamNotificationTarget


def test_get_team_notification_target_with_team_not_in_teams_table(db):
    targets = get_team_notification_targets("i_do_not_exist")
    assert targets.count() == 0


def test_test_get_team_notification_target(db):
    teams = sorted(["test-t1", "test-t2"])

    for team_name in teams:
        Team(name=team_name).save()

    for team in get_teams_from_db():
        TeamNotificationTarget(team=team, email=f"{team}@test.done").save()

    for team_name in teams:
        target_team = get_team_notification_targets(team=team_name)

        assert target_team[0].team.name == team_name
        assert target_team[0].red_alerts_only == False
