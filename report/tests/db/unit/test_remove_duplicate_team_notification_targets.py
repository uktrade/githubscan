# -*- coding: utf-8 -*-
from report.models import Team, TeamNotificationTarget, SAMLNotificationTarget
from report.db import (
    remove_duplicate_team_notification_targets,
    update_sso_notification_targets_in_db,
    update_teams_in_db,
)


def test_removing_duplicate_from_team_notification(
    db, report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data
    notification_targets = report_reader.sso_notification_targets

    github_teams = list(report_reader.teams.keys())

    update_teams_in_db(github_teams=github_teams)
    update_sso_notification_targets_in_db(sso_notification_targets=notification_targets)

    duplicated_targets = {}

    for team in github_teams:
        team_obj = Team.objects.get(name=team)

        if notification_targets[team]:
            login = list(notification_targets[team].keys())[0]
            email = notification_targets[team][login]
            TeamNotificationTarget(team=team_obj, email=email).save()
            duplicated_targets.update({team: email})

    # Manaual Target to ensure it stays after the removal of oters
    TeamNotificationTarget(
        team=Team.objects.get(name="team1"), email="anything@but.ordinary"
    ).save()

    # lets assert targets are in both SSO and Manual targets
    for team in github_teams:
        if notification_targets[team]:
            email = duplicated_targets[team]

            assert (
                TeamNotificationTarget.objects.filter(team=team, email=email).count()
                == 1
            )
            assert (
                SAMLNotificationTarget.objects.filter(team=team, email=email).count()
                == 1
            )

    remove_duplicate_team_notification_targets()

    # Lets assert targets are in SSO targets but not in Manaual/TeamNotification Targets

    for team in github_teams:
        if notification_targets[team]:
            email = duplicated_targets[team]

            assert (
                TeamNotificationTarget.objects.filter(team=team, email=email).count()
                == 0
            )
            assert (
                SAMLNotificationTarget.objects.filter(team=team, email=email).count()
                == 1
            )

    # Lets assert unqie entry stays
    assert (
        TeamNotificationTarget.objects.filter(
            team="team1", email="anything@but.ordinary"
        ).count()
        == 1
    )
