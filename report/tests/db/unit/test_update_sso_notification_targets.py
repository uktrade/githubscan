# -*- coding: utf-8 -*-
from report.db import update_sso_notification_targets_in_db, update_teams_in_db
from report.models import SAMLNotificationTarget
from copy import deepcopy


def test_update_enterprise_users_in_db_with_wrong_data_type(db, caplog):
    try:
        sso_notification_targets = "target-to-fail"
        update_sso_notification_targets_in_db(
            sso_notification_targets=sso_notification_targets
        )
        assert False
    except TypeError:
        assert "sso_notification_targets expected to be hash but it is a str"
        assert True


def test_update_sso_notification_targets_in_db_with_mock_data(
    db, report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data

    notification_targets = report_reader.sso_notification_targets
    update_teams_in_db(github_teams=list(report_reader.teams.keys()))
    update_sso_notification_targets_in_db(sso_notification_targets=notification_targets)

    for team, target_info in notification_targets.items():
        notification_targets_in_db = SAMLNotificationTarget.objects.filter(team=team)

        for target in notification_targets_in_db:
            if target_info:
                assert target.login in target_info
                assert target.email == target_info[target.login]


def test_update_sso_notification_targets_in_db_with_cascade_team_delete(
    db, report_reader, data_index, processed_data
):
    report_reader.load_data_from_dict = processed_data

    notification_targets = deepcopy(report_reader.sso_notification_targets)

    update_teams_in_db(github_teams=list(report_reader.teams.keys()))
    update_sso_notification_targets_in_db(sso_notification_targets=notification_targets)

    del notification_targets["team4"]

    update_teams_in_db(github_teams=list(notification_targets.keys()))

    new_teams = SAMLNotificationTarget.objects.values_list("team", flat=True)

    assert "team4" not in new_teams


def test_update_sso_notification_targets_in_db_with_delete_user(
    db, report_reader, data_index, processed_data
):
    report_reader.load_data_from_dict = processed_data

    notification_targets = deepcopy(report_reader.sso_notification_targets)

    update_teams_in_db(github_teams=list(report_reader.teams.keys()))
    update_sso_notification_targets_in_db(sso_notification_targets=notification_targets)

    logins = list(notification_targets["team3"].keys())

    del_login = logins[0]
    del notification_targets["team3"][del_login]

    update_sso_notification_targets_in_db(sso_notification_targets=notification_targets)

    logins_in_db = list(
        SAMLNotificationTarget.objects.filter(team="team3").values_list(
            "login", flat=True
        )
    )

    assert del_login not in logins_in_db
