# -*- coding: utf-8 -*-
import email
from common.functions import is_valid_email


def test_email_with_invalid_domain():
    email = "user1@test."
    assert is_valid_email(email=email) == False


def test_email_with_no_domain():
    email = "user.1.1.1.1"
    assert is_valid_email(email=email) == False


def test_email_with_valid_email():
    email = "user1@test.com"
    assert is_valid_email(email=email) == True
