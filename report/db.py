# -*- coding: utf-8 -*-
from itertools import combinations

from common.functions import isinstance_of
from report.models import (
    EnterpriseUser,
    OrganizationNotificationTarget,
    SAMLNotificationTarget,
    Team,
    TeamNotificationTarget,
)


def update_enterprise_users_in_db(enterprise_users):
    "Update enterprise users"

    isinstance_of(enterprise_users, dict, "enterprise_users")

    enterprise_users_in_db = set(EnterpriseUser.objects.values_list("login", flat=True))
    enterprise_users_in_github = set(enterprise_users.keys())

    add_records = enterprise_users_in_github.difference(enterprise_users_in_db)
    remove_records = enterprise_users_in_db.difference(enterprise_users_in_github)

    EnterpriseUser.objects.filter(login__in=remove_records).delete()

    for record in add_records:
        EnterpriseUser(
            login=record,
            email=enterprise_users[record]["email"],
            name=enterprise_users[record]["name"],
        ).save()


def update_sso_notification_targets_in_db(sso_notification_targets):
    isinstance_of(sso_notification_targets, dict, "sso_notification_targets")

    for team in sso_notification_targets.keys():
        team_obj = Team.objects.get(name=team)

        """
        If team does not have any members just add blank and save
        """
        if not sso_notification_targets[team] and team not in list(
            SAMLNotificationTarget.objects.values_list("team", flat=True)
        ):
            SAMLNotificationTarget(team=team_obj, login="", email="").save()
            continue

        members_in_db = set(
            SAMLNotificationTarget.objects.filter(team=team).values_list(
                "login", flat=True
            )
        )
        members_in_github = set(sso_notification_targets[team].keys())

        add_records = members_in_github.difference(members_in_db)
        remove_records = members_in_db.difference(members_in_github)

        for login in remove_records:
            SAMLNotificationTarget.objects.filter(team=team, login=login).delete()

        for login in add_records:
            email = sso_notification_targets[team][login]
            SAMLNotificationTarget(team=team_obj, login=login, email=email).save()


def remove_duplicate_team_notification_targets():
    for team in Team.objects.all():
        notification_targets = set(
            TeamNotificationTarget.objects.filter(team=team).values_list(
                "email", flat=True
            )
        )
        sso_notification_targets = set(
            SAMLNotificationTarget.objects.filter(team=team).values_list(
                "email", flat=True
            )
        )
        remove_records = sso_notification_targets.intersection(notification_targets)

        for email in remove_records:
            notification_obj = TeamNotificationTarget.objects.filter(
                team=team, email=email
            ).get()
            TeamNotificationTarget(id=notification_obj.id).delete()


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


def get_enterprise_users_from_db():
    return EnterpriseUser.objects.all()


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
    saml_targets = SAMLNotificationTarget.objects.filter(team=team).exclude(email="")
    team_targets = TeamNotificationTarget.objects.filter(team=team).exclude(email="")

    return saml_targets.union(team_targets)

    # return SAMLNotificationTarget.objects.filter(team=team).union(
    #     TeamNotificationTarget.objects.filter(team=team)
    # )


def get_organization_notification_targets():
    """
    Returns emails for organization level reports
    """
    return OrganizationNotificationTarget.objects.all()


def get_reportable_organization_notification_targets():
    """
    Returns reportable email for organization level report
    """
    return OrganizationNotificationTarget.objects.filter(reporting_enabled=True).all()
