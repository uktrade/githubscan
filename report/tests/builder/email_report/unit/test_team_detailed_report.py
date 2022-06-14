# -*- coding: utf-8 -*-
import re


def test_team_detailed_subject(
    build_email_report, report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data

    team1_email_report = build_email_report.team_detailed(
        team="team1", report_reader=report_reader
    )
    team2_email_report = build_email_report.team_detailed(
        team="team2", report_reader=report_reader
    )
    team3_email_report = build_email_report.team_detailed(
        team="team3", report_reader=report_reader
    )
    team4_email_report = build_email_report.team_detailed(
        team="team4", report_reader=report_reader
    )

    if data_index == 1:
        assert re.search("2 Vulnerable packages - Team1", team1_email_report["subject"])
        assert re.search("4 Vulnerable packages - Team2", team2_email_report["subject"])
        assert re.search("2 Vulnerable packages - Team3", team3_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team4", team4_email_report["subject"])

    if data_index == 2:
        assert re.search("2 Vulnerable packages - Team1", team1_email_report["subject"])
        assert re.search("4 Vulnerable packages - Team2", team2_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team3", team3_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team4", team4_email_report["subject"])

    if data_index == 3:
        assert re.search("2 Vulnerable packages - Team1", team1_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team2", team2_email_report["subject"])
        assert re.search("2 Vulnerable packages - Team3", team3_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team4", team4_email_report["subject"])

    if data_index == 4:
        assert re.search("2 Vulnerable packages - Team1", team1_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team2", team2_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team3", team3_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team4", team4_email_report["subject"])

    if data_index == 5:
        assert re.search("0 Vulnerable packages - Team1", team1_email_report["subject"])
        assert re.search("4 Vulnerable packages - Team2", team2_email_report["subject"])
        assert re.search("2 Vulnerable packages - Team3", team3_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team4", team4_email_report["subject"])

    if data_index == 6:
        assert re.search("0 Vulnerable packages - Team1", team1_email_report["subject"])
        assert re.search("4 Vulnerable packages - Team2", team2_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team3", team3_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team4", team4_email_report["subject"])

    if data_index == 7:
        assert re.search("0 Vulnerable packages - Team1", team1_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team2", team2_email_report["subject"])
        assert re.search("2 Vulnerable packages - Team3", team3_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team4", team4_email_report["subject"])

    if data_index == 8:
        assert re.search("0 Vulnerable packages - Team1", team1_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team2", team2_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team3", team3_email_report["subject"])
        assert re.search("0 Vulnerable packages - Team4", team4_email_report["subject"])

    report_reader.clear()
