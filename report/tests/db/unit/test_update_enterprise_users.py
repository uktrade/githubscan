# -*- coding: utf-8 -*-
from report.db import update_enterprise_users_in_db
from report.models import EnterpriseUser

enterprise_users = {
    "user1": {"email": "user1@test.com", "name": "User One"},
    "user2": {"email": "user2@test.com", "name": "User Two"},
    "user3": {"email": "user3@test.com", "name": "User Three"},
    "user4": {"email": "user4@test.com", "name": "User Four"},
    "user5": {"email": "user5@test.com", "name": "User Five"},
    "user6": {"email": "user6@test.com", "name": "User Six"},
}


def test_update_enterprise_users_in_db_with_wrong_data_type(db, caplog):
    try:
        eneterprise_users = "test-t1"
        update_enterprise_users_in_db(eneterprise_users=eneterprise_users)
        assert False
    except TypeError:
        assert "eneterprise_users expected to be hash but it is a str"
        assert True


def test_update_enterprise_users_in_db_with_data(db):
    global enterprise_users

    update_enterprise_users_in_db(enterprise_users=enterprise_users)

    users_in_db = EnterpriseUser.objects.values_list("email", flat=True)

    assert len(enterprise_users) == len(users_in_db)


def test_update_enterprise_users_in_db_it_removes_users_from_db(db):

    global enterprise_users

    update_enterprise_users_in_db(enterprise_users=enterprise_users)

    users_in_db = list(EnterpriseUser.objects.values_list("email", flat=True))

    new_enterprise_users = {
        "user3": {"email": "user3@test.com", "name": "User Three"},
        "user4": {"email": "user4@test.com", "name": "User Four"},
        "user5": {"email": "user5@test.com", "name": "User Five"},
        "user6": {"email": "user6@test.com", "name": "User Six"},
    }

    update_enterprise_users_in_db(enterprise_users=new_enterprise_users)

    new_users_in_db = list(EnterpriseUser.objects.values_list("email", flat=True))

    assert "user1@test.com" in users_in_db
    assert "user2@test.com" in users_in_db

    assert "user1@test.com" not in new_users_in_db
    assert "user2@test.com" not in new_users_in_db

    assert len(users_in_db) == len(enterprise_users)
    assert len(new_users_in_db) == len(new_enterprise_users)
