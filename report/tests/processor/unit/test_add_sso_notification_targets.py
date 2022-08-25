# -*- coding: utf-8 -*-
def test_add_sso_notification_targets(processor, scene_index, scene_data):
    """test it for all scenarios"""
    processor.load_data_from_dict = scene_data
    processor.add_sso_notification_targets()

    check_sso_notification_targets(
        sso_notification_targets=processor.sso_notification_targets
    )
    check_users_without_sso_email(
        users_without_sso_email=processor.users_without_sso_email
    )

    processor.clear()


def check_sso_notification_targets(sso_notification_targets):

    assert "user1" in sso_notification_targets["team1"]
    assert "user2" in sso_notification_targets["team1"]

    assert "user2" in sso_notification_targets["team2"]
    assert "user3" in sso_notification_targets["team2"]

    assert "user4" in sso_notification_targets["team3"]
    assert "user5" in sso_notification_targets["team3"]
    assert "user6" in sso_notification_targets["team3"]

    assert len(sso_notification_targets["team4"]) == 0


def check_users_without_sso_email(users_without_sso_email):

    assert "user7" in users_without_sso_email
    assert "user9" in users_without_sso_email

    assert len(users_without_sso_email) == 2
