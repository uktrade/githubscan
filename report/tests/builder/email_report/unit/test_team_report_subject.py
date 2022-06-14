# -*- coding: utf-8 -*-
from config.severities import SEVERITY_STATUS


def test_teams_exception(build_email_report, report_reader, data_index, processed_data):
    report_reader.load_data_from_dict = processed_data

    try:
        team1_email_report = build_email_report.teams_summary(
            team="team_does_not_exist", report_reader=report_reader
        )
        report_reader.clear()
        assert False
    except ValueError:
        assert True


def test_team_report_subject(
    build_email_report, report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data

    team1_email_report = build_email_report.teams_summary(
        team="team1", report_reader=report_reader
    )
    team2_email_report = build_email_report.teams_summary(
        team="team2", report_reader=report_reader
    )
    team3_email_report = build_email_report.teams_summary(
        team="team3", report_reader=report_reader
    )
    team4_email_report = build_email_report.teams_summary(
        team="team4", report_reader=report_reader
    )

    if data_index == 1:
        assert (
            team1_email_report["subject"]
            == f"[{SEVERITY_STATUS.RED.name}] Daily: Github Team1 team Vulnerabilities Scan Report"
        )
        assert (
            team2_email_report["subject"]
            == f"[{SEVERITY_STATUS.AMBER.name}] Daily: Github Team2 team Vulnerabilities Scan Report"
        )
        assert (
            team3_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team3 team Vulnerabilities Scan Report"
        )
        assert (
            team4_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team4 team Vulnerabilities Scan Report"
        )

    if data_index == 2:
        assert (
            team1_email_report["subject"]
            == f"[{SEVERITY_STATUS.RED.name}] Daily: Github Team1 team Vulnerabilities Scan Report"
        )
        assert (
            team2_email_report["subject"]
            == f"[{SEVERITY_STATUS.AMBER.name}] Daily: Github Team2 team Vulnerabilities Scan Report"
        )
        assert (
            team3_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team3 team Vulnerabilities Scan Report"
        )
        assert (
            team4_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team4 team Vulnerabilities Scan Report"
        )

    if data_index == 3:
        assert (
            team1_email_report["subject"]
            == f"[{SEVERITY_STATUS.RED.name}] Daily: Github Team1 team Vulnerabilities Scan Report"
        )
        assert (
            team2_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team2 team Vulnerabilities Scan Report"
        )
        assert (
            team3_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team3 team Vulnerabilities Scan Report"
        )
        assert (
            team4_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team4 team Vulnerabilities Scan Report"
        )

    if data_index == 4:
        assert (
            team1_email_report["subject"]
            == f"[{SEVERITY_STATUS.RED.name}] Daily: Github Team1 team Vulnerabilities Scan Report"
        )
        assert (
            team2_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team2 team Vulnerabilities Scan Report"
        )
        assert (
            team3_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team3 team Vulnerabilities Scan Report"
        )
        assert (
            team4_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team4 team Vulnerabilities Scan Report"
        )

    if data_index == 5:
        assert (
            team1_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team1 team Vulnerabilities Scan Report"
        )
        assert (
            team2_email_report["subject"]
            == f"[{SEVERITY_STATUS.AMBER.name}] Daily: Github Team2 team Vulnerabilities Scan Report"
        )
        assert (
            team3_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team3 team Vulnerabilities Scan Report"
        )
        assert (
            team4_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team4 team Vulnerabilities Scan Report"
        )

    if data_index == 6:
        assert (
            team1_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team1 team Vulnerabilities Scan Report"
        )
        assert (
            team2_email_report["subject"]
            == f"[{SEVERITY_STATUS.AMBER.name}] Daily: Github Team2 team Vulnerabilities Scan Report"
        )
        assert (
            team3_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team3 team Vulnerabilities Scan Report"
        )
        assert (
            team4_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team4 team Vulnerabilities Scan Report"
        )

    if data_index == 7 or data_index == 8:
        assert (
            team1_email_report["subject"]
            == f"[{SEVERITY_STATUS.GREEN.name}] Daily: Github Team1 team Vulnerabilities Scan Report"
        )

    report_reader.clear()
