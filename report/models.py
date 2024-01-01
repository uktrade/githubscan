# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.deletion import CASCADE


class EnterpriseUser(models.Model):
    login = models.CharField(primary_key=True, max_length=100)
    email = models.EmailField()
    name = models.CharField(blank=True, max_length=100)

    class Meta:
        app_label = "report"


class Team(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    reporting_enabled = models.BooleanField(
        default=True,
        help_text="Set True (checked / on) to enable reporting for this team.",
    )

    class Meta:
        app_label = "report"


class TeamNotificationTarget(models.Model):
    team = models.ForeignKey(
        "Team",
        on_delete=CASCADE,
    )
    login = models.CharField(max_length=30, default="", blank=True)
    email = models.EmailField(
        help_text="Target email address for team-level notifications.",
    )

    red_alerts_only = models.BooleanField(
        default=False,
        help_text=(
            "Set True (checked/on) to prevent green status notifications being " "sent."
        ),
    )

    no_green_alerts = models.BooleanField(
        default=False,
        help_text=("Set False (checked/on) to receive green status notifications"),
    )

    class Meta:
        unique_together = ("team", "email")
        app_label = "report"

    def __str__(self):
        return f"{self.team}:{self.email}"


class SAMLNotificationTarget(models.Model):
    team = models.ForeignKey(
        "Team",
        on_delete=CASCADE,
    )

    login = models.CharField(max_length=30)

    email = models.EmailField(
        blank=True,
        help_text="Target email address obtail from SAML for team-level notifications.",
    )

    red_alerts_only = models.BooleanField(
        default=False,
        help_text=(
            "Set True (checked/on) to prevent green status notifications being " "sent."
        ),
    )

    no_green_alerts = models.BooleanField(
        default=True,
        help_text=("Set False (checked/on) to receive green status notifications"),
    )

    class Meta:
        unique_together = ("team", "email")
        app_label = "report"

    def __str__(self):
        return f"{self.team}:{self.email}"


class OrganizationNotificationTarget(models.Model):
    email = models.EmailField(
        primary_key=True, help_text="Target email address for Organization Level Email"
    )
    reporting_enabled = models.BooleanField(
        default=True,
        help_text="Set it to False (unchecked/off) to disable email notifications",
    )

    class Meta:
        app_label = "report"
