# -*- coding: utf-8 -*-
from report.report import create_processed_data
import report.tests.processor.unit as report_checks
from config.schema import processed_data_schema


def test_create_report(db, scene_index, scene_data):

    processed_data = create_processed_data(scanner_data=scene_data)

    assert processed_data_schema.is_valid(processed_data)

    repositories = processed_data["repositories"]

    organization_total = processed_data["total"]
    organization_severity_status = processed_data["severity_status"]
    organization_vulnerable_repositories = processed_data["vulnerable_repositories"]

    teams = processed_data["teams"]

    orhpan_repositories = processed_data["orphan_repositories"]
    skip_scan_repositories = processed_data["skip_scan_repositories"]

    """
    test alerts level report
    """
    report_checks.check_effective_level_and_escalation_status(repositories=repositories)
    report_checks.check_fix_by_date(repositories=repositories)
    report_checks.check_severity_age_in_days(repositories=repositories)

    """
    check repository teams
    """
    report_checks.check_add_repository_teams(repositories=repositories)

    """
    test organization level report
    """
    report_checks.check_organization_totals_vulnerable_repositories(
        scene_index=scene_index,
        vulnerable_repositories=organization_total["repositories"],
    )
    report_checks.check_organization_severity_status(
        scene_index=scene_index, severity_status=organization_severity_status
    )
    report_checks.check_organization_totals_severities(
        scene_index=scene_index, severities=organization_total["severities"]
    )
    report_checks.check_organization_totals_slo_breaches(
        scene_index=scene_index, slo_breach=organization_total["slo_breach"]
    )

    """
    test orphan repositories level report
    """
    report_checks.check_orphan_totals_vulnerable_repositoriest(
        scene_index=scene_index,
        vulnerable_repositories_count=orhpan_repositories["total"]["repositories"],
    )
    report_checks.check_orphan_repositories_totals_severities(
        scene_index=scene_index,
        severities=orhpan_repositories["total"]["severities"],
    )
    report_checks.check_orphan_repositories_totals_slo_breaches(
        scene_index=scene_index,
        slo_breach=orhpan_repositories["total"]["slo_breach"],
    )
    report_checks.check_orphan_repositories_severity_status(
        scene_index=scene_index,
        severity_status=orhpan_repositories["severity_status"],
    )
    report_checks.check_orphan_repositorie(
        orphan_repositories_list=orhpan_repositories["list"]
    )

    """
    test repoistory level report
    """
    report_checks.check_repositores(repositories=repositories)
    report_checks.check_repository_severity_status(
        scene_index=scene_index, repositories=repositories
    )
    report_checks.check_repository_totals(
        scene_index=scene_index, repositories=repositories
    )

    """
    test skip scan repositories
    """
    report_checks.check_skip_scan_totals_vulnerable_repositoriest(
        scene_index=scene_index,
        vulnerable_repositories_count=skip_scan_repositories["total"]["repositories"],
    )
    report_checks.check_skip_scan_repositories_total_severitie(
        scene_index=scene_index,
        severities=skip_scan_repositories["total"]["severities"],
    )
    report_checks.check_skip_scan_repositories(
        repositories=repositories,
        skip_scan_repositories_list=skip_scan_repositories["list"],
    )
    report_checks.check_skip_scan_repositories_severity_status(
        scene_index=scene_index,
        severity_status=skip_scan_repositories["severity_status"],
    )
    report_checks.check_skip_scan_repositories_slo_breach_totals(
        scene_index=scene_index,
        slo_breach=skip_scan_repositories["total"]["slo_breach"],
    )

    """
    Test teams level report
    """
    report_checks.check_team_severity_status(scene_index=scene_index, teams=teams)
    report_checks.check_team_totals_vulnerable_repositories(
        scene_index=scene_index, teams=teams
    )
    report_checks.check_team_total_severities(scene_index=scene_index, teams=teams)
    report_checks.check_team_total_slo_breach(scene_index=scene_index, teams=teams)

    report_checks.check_teams_and_team_repositories(teams=teams)

    """
    Test token has no access
    """
    report_checks.check_token_has_no_access(
        token_has_no_access=processed_data["token_has_no_access"]
    )

    """
    Test vulnerable repositories count
    """
    report_checks.check_vulnerable_repositories(
        scene_index=scene_index,
        vulnerable_repositories=organization_vulnerable_repositories,
    )

    processed_data.clear()
