# -*- coding: utf-8 -*-

from .test_add_enterprise_users import check_add_enterprise_users
from .test_add_sso_notification_targets import check_sso_notification_targets
from .test_add_sso_notification_targets import check_users_without_sso_email

"""
Import alerts check
"""
from .test_add_effective_level_and_esclation_status import (
    check_effective_level_and_escalation_status,
)

from .test_add_repository_teams import check_add_repository_teams

from .test_add_fix_by_date import check_fix_by_date

from .test_add_severity_age_in_days import check_severity_age_in_days

"""
Import Oranization level check
"""
from .test_add_organization_totals_vulnerable_repositories import (
    check_organization_totals_vulnerable_repositories,
)
from .test_add_organization_totals_slo_breaches import (
    check_organization_totals_slo_breaches,
)
from .test_add_organization_severity_status import check_organization_severity_status
from .test_add_organization_totals_severities import (
    check_organization_totals_severities,
)

"""
Import Orphan repositories check
"""
from .test_add_orphan_totals_vulnerable_repositories import (
    check_orphan_totals_vulnerable_repositoriest,
)
from .test_add_orphan_repositories_totals_severities import (
    check_orphan_repositories_totals_severities,
)
from .test_add_orphan_repositories_totals_slo_breaches import (
    check_orphan_repositories_totals_slo_breaches,
)
from .test_add_orphan_repositories_severity_status import (
    check_orphan_repositories_severity_status,
)
from .test_add_orphan_repositories import check_orphan_repositorie

"""
Import repository check
"""
from .test_add_repositories import check_repositores
from .test_add_repository_severity_status import check_repository_severity_status
from .test_add_repository_totals import check_repository_totals


"""
Import  checks for repository with skip scan True
"""
from .test_add_skip_scan_totals_vulnerable_repositoriest import (
    check_skip_scan_totals_vulnerable_repositoriest,
)
from .test_add_skip_scan_repositories import check_skip_scan_repositories
from .test_add_skip_scan_repositories_total_severities import (
    check_skip_scan_repositories_total_severitie,
)
from .test_add_skip_scan_repositories_severity_status import (
    check_skip_scan_repositories_severity_status,
)
from .test_add_skip_scan_repositories_slo_breach_totals import (
    check_skip_scan_repositories_slo_breach_totals,
)

"""
Import teams check
"""
from .test_add_team_severity_status import check_team_severity_status
from .test_add_team_totals_vulnerable_repositories import (
    check_team_totals_vulnerable_repositories,
)
from .test_add_team_total_severities import check_team_total_severities
from .test_add_team_total_slo_breach import check_team_total_slo_breach

"""
Import teams and teams repository checks
"""
from .test_add_teams_and_team_repositories import check_teams_and_team_repositories

"""
Import Token has no access checks
"""
from .test_add_token_has_no_access import check_token_has_no_access

"""
Import vulnerable repositories
"""
from .test_add_vulnurable_repositories import check_vulnerable_repositories


__all__ = [
    "check_add_enterprise_users",
    "check_effective_level_and_escalation_status",
    "check_add_repository_teams",
    "check_fix_by_date",
    "check_severity_age_in_days",
    "check_organization_totals_vulnerable_repositories",
    "check_organization_severity_status",
    "check_organization_totals_severities",
    "check_organization_totals_slo_breaches",
    "check_orphan_totals_vulnerable_repositoriest",
    "check_orphan_repositories_totals_severities",
    "check_orphan_repositories_totals_slo_breaches",
    "check_orphan_repositories_severity_status",
    "check_orphan_repositorie",
    "check_repositores",
    "check_repository_severity_status",
    "check_repository_totals",
    "check_skip_scan_totals_vulnerable_repositoriest",
    "check_skip_scan_repositories",
    "check_skip_scan_repositories_total_severitie",
    "check_skip_scan_repositories_severity_status",
    "check_skip_scan_repositories_slo_breach_totals",
    "check_team_severity_status",
    "check_team_totals_vulnerable_repositories",
    "check_team_total_severities",
    "check_team_total_slo_breach",
    "check_teams_and_team_repositories",
    "check_token_has_no_access",
    "check_vulnerable_repositories",
    "check_sso_notification_targets",
    "check_users_without_sso_email",
]
