# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.deletion import CASCADE


class Team(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    reporting_enabled = models.BooleanField(
        default=True,
        help_text="Set True (checked / on) to enable reporting for this team.",
    )


class TeamNotificationTarget(models.Model):
    team = models.ForeignKey(
        "Team",
        on_delete=CASCADE,
    )
    email = models.EmailField(
        help_text="Target email address for team-level notifications.",
    )
    red_alerts_only = models.BooleanField(
        default=False,
        help_text=(
            "Set True (checked/on) to prevent green status notifications being " "sent."
        ),
    )

    class Meta:
        unique_together = ("team", "email")

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
