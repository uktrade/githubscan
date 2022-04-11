# -*- coding: utf-8 -*-
import re

import re


def test_organization_slo_breach(
    build_slack_report, report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data

    build_slack_report.organization_slo_breach(report_reader=report_reader)

    assert (
        build_slack_report.slack_message[0]["text"]["text"]
        == "Github Organization SLO Breach report summary"
    )

    TOTAL_REPOSITORY_TEXT = f'{"Total Repositories:":22s}'

    if data_index == 1 or data_index == 2:
        assert re.search(
            f"{TOTAL_REPOSITORY_TEXT}{8:3d}",
            build_slack_report.slack_message[1]["text"]["text"],
        )

    if data_index == 3 or data_index == 4:
        assert re.search(
            f"{TOTAL_REPOSITORY_TEXT}{3:3d}",
            build_slack_report.slack_message[1]["text"]["text"],
        )

    if data_index == 5 or data_index == 6:
        assert re.search(
            f"{TOTAL_REPOSITORY_TEXT}{5:3d}",
            build_slack_report.slack_message[1]["text"]["text"],
        )

    if data_index == 7 or data_index == 8:
        assert re.search(
            f"{TOTAL_REPOSITORY_TEXT}{0:3d}",
            build_slack_report.slack_message[1]["text"]["text"],
        )

    build_slack_report.clear()
    report_reader.clear()
