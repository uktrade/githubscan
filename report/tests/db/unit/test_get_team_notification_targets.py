# -*- coding: utf-8 -*-
import email
from report.models import Team, TeamNotificationTarget, SAMLNotificationTarget
from report.db import (
    update_teams_in_db,
    update_sso_notification_targets_in_db,
    get_team_notification_targets,
)


def test_get_team_notification_targets(db, report_reader, data_index, processed_data):

    report_reader.load_data_from_dict = processed_data
    notification_targets = report_reader.sso_notification_targets

    github_teams = list(report_reader.teams.keys())

    update_teams_in_db(github_teams=github_teams)
    update_sso_notification_targets_in_db(sso_notification_targets=notification_targets)

    # Manaual Target to ensure it gets picked
    TeamNotificationTarget(
        team=Team.objects.get(name=github_teams[0]), email="anything@but.ordinary"
    ).save()

    for index, team in enumerate(github_teams):

        combined_targets = get_team_notification_targets(team=team)

        target_emails_in_db = list(
            filter(None, list(combined_targets.values_list("email", flat=True)))
        )

        if index == 0:
            assert "anything@but.ordinary" in target_emails_in_db
            assert (
                combined_targets.count() == len(notification_targets[team].keys()) + 1
            )

        else:
            assert len(target_emails_in_db) == len(notification_targets[team])

        for login, email in notification_targets[team].items():
            assert email in target_emails_in_db
