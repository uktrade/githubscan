# -*- coding: utf-8 -*-
import report.tests.processor.unit as report_checks


def test_report_reader(report_reader, data_index, processed_data):
    """
    Simply test if we have all the properties behaving as expected
    """
    report_reader.load_data_from_dict = processed_data
    """
    Test alerts
    """
    report_checks.check_effective_level_and_escalation_status(
        repositories=report_reader.repositories
    )
    report_checks.check_fix_by_date(repositories=report_reader.repositories)
    report_checks.check_severity_age_in_days(repositories=report_reader.repositories)

    """
    Test Vulnerable repositories
    """
    report_checks.check_vulnerable_repositories(
        scene_index=data_index,
        vulnerable_repositories=report_reader.vulnerable_repositories,
    )

    """
    Test Token has no access
    """
    report_checks.check_token_has_no_access(
        token_has_no_access=report_reader.token_has_no_access
    )
    report_checks.check_teams_and_team_repositories(teams=report_reader.teams)

    """
    Test Repositories
    """
    report_checks.check_repositores(repositories=report_reader.repositories)
    report_checks.check_repository_severity_status(
        scene_index=data_index, repositories=report_reader.repositories
    )
    report_checks.check_repository_totals(
        scene_index=data_index, repositories=report_reader.repositories
    )

    """
    Test Skip scan
    """
    report_checks.check_skip_scan_repositories(
        repositories=report_reader.repositories,
        skip_scan_repositories_list=report_reader.skip_scan_repositories,
    )

    report_checks.check_skip_scan_repositories_severity_status(
        scene_index=data_index,
        severity_status=report_reader.skip_scan_repositories["severity_status"],
    )
    report_checks.check_skip_scan_repositories_slo_breach_totals(
        scene_index=data_index,
        slo_breach=report_reader.skip_scan_repositories["total"]["slo_breach"],
    )
    report_checks.check_skip_scan_repositories_total_severitie(
        scene_index=data_index,
        severities=report_reader.skip_scan_repositories["total"]["severities"],
    )
    report_checks.check_skip_scan_totals_vulnerable_repositoriest(
        scene_index=data_index,
        vulnerable_repositories_count=report_reader.skip_scan_repositories["total"][
            "repositories"
        ],
    )

    """
    Test orphan repositories
    """
    report_checks.check_orphan_repositorie(
        orphan_repositories_list=report_reader.orphan_repositories["list"]
    )
    report_checks.check_orphan_repositories_severity_status(
        scene_index=data_index,
        severity_status=report_reader.orphan_repositories["severity_status"],
    )
    report_checks.check_orphan_repositories_totals_severities(
        scene_index=data_index,
        severities=report_reader.orphan_repositories["total"]["severities"],
    )
    report_checks.check_orphan_repositories_totals_slo_breaches(
        scene_index=data_index,
        slo_breach=report_reader.orphan_repositories["total"]["slo_breach"],
    )
    report_checks.check_orphan_totals_vulnerable_repositoriest(
        scene_index=data_index,
        vulnerable_repositories_count=report_reader.orphan_repositories["total"][
            "repositories"
        ],
    )

    """
    Test Organization data
    """

    report_checks.check_organization_severity_status(
        scene_index=data_index,
        severity_status=report_reader.organization_severity_status,
    )
    report_checks.check_organization_totals_severities(
        scene_index=data_index,
        severities=report_reader.organization_total["severities"],
    )
    report_checks.check_organization_totals_slo_breaches(
        scene_index=data_index,
        slo_breach=report_reader.organization_total["slo_breach"],
    )
    report_checks.check_organization_totals_vulnerable_repositories(
        scene_index=data_index,
        vulnerable_repositories=report_reader.organization_total["repositories"],
    )

    """
    Test teams
    """
    report_checks.check_teams_and_team_repositories(teams=report_reader.teams)
    report_checks.check_team_severity_status(
        scene_index=data_index, teams=report_reader.teams
    )
    report_checks.check_team_total_severities(
        scene_index=data_index, teams=report_reader.teams
    )
    report_checks.check_team_total_slo_breach(
        scene_index=data_index, teams=report_reader.teams
    )
    report_checks.check_team_totals_vulnerable_repositories(
        scene_index=data_index, teams=report_reader.teams
    )

    report_reader.clear()
