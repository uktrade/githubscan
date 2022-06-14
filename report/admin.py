# -*- coding: utf-8 -*-
from django.contrib import admin
from report.models import Team, TeamNotificationTarget, OrganizationNotificationTarget


@admin.register(TeamNotificationTarget)
class TeamNotificationTargetAdmin(admin.ModelAdmin):
    list_display = ("id", "team", "red_alerts_only")


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "reporting_enabled")


@admin.register(OrganizationNotificationTarget)
class OrganizationNotificationTargetAdmin(admin.ModelAdmin):
    list_display = ("email", "reporting_enabled")
