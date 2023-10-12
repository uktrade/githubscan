# -*- coding: utf-8 -*-
from django.contrib import admin

from report.models import (
    EnterpriseUser,
    OrganizationNotificationTarget,
    SAMLNotificationTarget,
    Team,
    TeamNotificationTarget,
)


@admin.register(EnterpriseUser)
class EnterpriseUserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "login")
    search_fields = ("email", "name", "login")
    ordering = ("email",)


@admin.register(TeamNotificationTarget)
class TeamNotificationTargetAdmin(admin.ModelAdmin):
    list_display = (
        "get_team_name",
        "email",
        "red_alerts_only",
        "no_green_alerts",
    )

    def get_team_name(self, obj):
        return obj.team.name

    get_team_name.short_description = "Team"
    get_team_name.admin_order_field = "team__name"


@admin.register(SAMLNotificationTarget)
class SAMLNotificationTargetAdmin(admin.ModelAdmin):
    list_display = (
        "get_team_name",
        "login",
        "email",
        "red_alerts_only",
        "no_green_alerts",
    )

    def get_team_name(self, obj):
        return obj.team.name

    get_team_name.short_description = "Team"
    get_team_name.admin_order_field = "team__name"


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("name", "reporting_enabled")
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(OrganizationNotificationTarget)
class OrganizationNotificationTargetAdmin(admin.ModelAdmin):
    list_display = ("email", "reporting_enabled")
    search_fields = ("email",)
    ordering = ("email",)
