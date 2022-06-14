# -*- coding: utf-8 -*-
from report.models import Team, TeamNotificationTarget, OrganizationNotificationTarget
from common.functions import isinstance_of


def update_teams_in_db(github_teams):
    """
    Adds team to db
    """
    isinstance_of(github_teams, list, "github_teams")

    teams_in_db = set(Team.objects.values_list("name", flat=True))
    teams_in_github = set(github_teams)

    add_records = teams_in_github.difference(teams_in_db)
    remove_rcords = teams_in_db.difference(teams_in_github)

    Team.objects.filter(name__in=remove_rcords).delete()

    for record in add_records:
        Team(name=record).save()


def get_teams_from_db():
    """
    Returns all teams
    """
    return Team.objects.all()


def get_reportable_teams_from_db():
    """
    Retruns teams with reporting_enabled set to True
    """
    return Team.objects.filter(reporting_enabled=True).all()


def get_team_notification_targets(team):
    return TeamNotificationTarget.objects.filter(team=team).all()


def get_organization_notification_targets():
    """
    Returns emails for organization level reports
    """
    return OrganizationNotificationTarget.objects.all()


def get_repotable_organization_notification_targets():
    """
    Returns reportable email for organization level report
    """
    return OrganizationNotificationTarget.objects.filter(reporting_enabled=True).all()
