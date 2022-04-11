# -*- coding: utf-8 -*-
from config.severities import SEVERITY_STATUS


def test_add_team_severity_status(processor, scene_index, scene_data):
    """
    test it for all scenarios
    """

    processor.load_data_from_dict = scene_data
    processor.add_repositories()
    processor.add_vulnerable_repositories()
    processor.add_teams_and_team_repositories()
    processor.add_token_has_no_access()
    processor.add_severity_age_in_days()
    processor.add_effective_level_and_escalation_status()
    processor.add_repository_severity_status()
    processor.add_skip_scan_repositories()
    processor.add_team_severity_status()

    check_team_severity_status(scene_index=scene_index, teams=processor.teams)

    processor.clear()


def check_team_severity_status(scene_index, teams):

    team1_severity_status = teams["team1"]["severity_status"]
    team2_severity_status = teams["team2"]["severity_status"]
    team3_severity_status = teams["team3"]["severity_status"]
    team4_severity_status = teams["team4"]["severity_status"]

    if scene_index == 1:
        team1_severity_status == SEVERITY_STATUS.RED.name
        team2_severity_status == SEVERITY_STATUS.AMBER.name
        team3_severity_status == SEVERITY_STATUS.GREEN.name
        team4_severity_status == SEVERITY_STATUS.CLEAN.name

    if scene_index == 2:
        team1_severity_status == SEVERITY_STATUS.RED.name
        team2_severity_status == SEVERITY_STATUS.AMBER.name
        team3_severity_status == SEVERITY_STATUS.AMBER.name
        team4_severity_status == SEVERITY_STATUS.CLEAN.name

    if scene_index == 3:
        team1_severity_status == SEVERITY_STATUS.RED.name
        team2_severity_status == SEVERITY_STATUS.CLEAN.name
        team3_severity_status == SEVERITY_STATUS.GREEN.name
        team4_severity_status == SEVERITY_STATUS.CLEAN.name

    if scene_index == 4:
        team1_severity_status == SEVERITY_STATUS.RED.name
        team2_severity_status == SEVERITY_STATUS.CLEAN.name
        team3_severity_status == SEVERITY_STATUS.CLEAN.name
        team4_severity_status == SEVERITY_STATUS.CLEAN.name

    if scene_index == 5:
        team1_severity_status == SEVERITY_STATUS.CLEAN.name
        team2_severity_status == SEVERITY_STATUS.AMBER.name
        team3_severity_status == SEVERITY_STATUS.GREEN.name
        team4_severity_status == SEVERITY_STATUS.CLEAN.name

    if scene_index == 6:
        team1_severity_status == SEVERITY_STATUS.CLEAN.name
        team2_severity_status == SEVERITY_STATUS.AMBER.name
        team3_severity_status == SEVERITY_STATUS.CLEAN.name
        team4_severity_status == SEVERITY_STATUS.CLEAN.name

    if scene_index == 7:
        team1_severity_status == SEVERITY_STATUS.CLEAN.name
        team2_severity_status == SEVERITY_STATUS.CLEAN.name
        team3_severity_status == SEVERITY_STATUS.GREEN.name
        team4_severity_status == SEVERITY_STATUS.CLEAN.name

    if scene_index == 8:
        team1_severity_status == SEVERITY_STATUS.CLEAN.name
        team2_severity_status == SEVERITY_STATUS.CLEAN.name
        team3_severity_status == SEVERITY_STATUS.CLEAN.name
        team4_severity_status == SEVERITY_STATUS.CLEAN.name
