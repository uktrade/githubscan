# -*- coding: utf-8 -*-
from report.db import get_reportable_organization_notification_targets
from report.models import OrganizationNotificationTarget


def test_get_reportable_organization_notification_targets_with_default_enabled(db):
    OrganizationNotificationTarget(email="test1@dummy.com").save()
    OrganizationNotificationTarget(email="test2@dummy.com").save()

    organization_targets = get_reportable_organization_notification_targets()

    sorted_targets = sorted(list(organization_targets.values_list("email", flat=True)))

    assert sorted_targets == ["test1@dummy.com", "test2@dummy.com"]


def test_get_reportable_organization_notification_targets_with_disabled_reporting(db):
    OrganizationNotificationTarget(
        email="test1@dummy.com", reporting_enabled=True
    ).save()
    OrganizationNotificationTarget(
        email="test2@dummy.com", reporting_enabled=False
    ).save()

    organization_targets = get_reportable_organization_notification_targets()

    sorted_targets = sorted(list(organization_targets.values_list("email", flat=True)))

    assert sorted_targets == ["test1@dummy.com"]
    assert "test2@dummy.com" not in sorted_targets

    assert organization_targets.get(email="test1@dummy.com").reporting_enabled == True
