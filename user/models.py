# -*- coding: utf-8 -*-
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_superuser(self, email_user_id, password, email=""):
        if email_user_id is None:
            raise ValueError("missing email address field")

        if password is None:
            raise ValueError("You must set password")

        email = email_user_id
        user = self.model(
            email=self.normalize_email(email), email_user_id=email_user_id
        )
        user.set_password(password)
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user


class User(AbstractUser):
    username = None

    email = models.EmailField(_("email address"), unique=True)
    email_user_id = models.EmailField(_("email address"), unique=True, blank=True)
    USERNAME_FIELD = "email_user_id"
    REQUIRED_FIELDS = []

    objects = UserManager()
