# -*- coding: utf-8 -*-
import re


def test_orphan_repositories_report(
    build_slack_report, report_reader, data_index, processed_data
):
    report_reader.load_data_from_dict = processed_data

    build_slack_report.orphan_repositories(report_reader=report_reader)

    assert (
        build_slack_report.slack_message[0]["text"]["text"]
        == "Github Orphan Repositories severity summary"
    )

    TOTAL_REPOSITORY_TEXT = f'{"Total Repositories:":22s}'

    if data_index == 1:
        assert re.search(
            f"{TOTAL_REPOSITORY_TEXT}{3:3d}",
            build_slack_report.slack_message[1]["text"]["text"],
        )

    if data_index == 2 or data_index == 3 or data_index == 5:
        assert re.search(
            f"{TOTAL_REPOSITORY_TEXT}{2:3d}",
            build_slack_report.slack_message[1]["text"]["text"],
        )

    if data_index == 4 or data_index == 6 or data_index == 7:
        assert re.search(
            f"{TOTAL_REPOSITORY_TEXT}{1:3d}",
            build_slack_report.slack_message[1]["text"]["text"],
        )

    if data_index == 0:
        assert re.search(
            f"{TOTAL_REPOSITORY_TEXT}{0:3d}",
            build_slack_report.slack_message[1]["text"]["text"],
        )

    build_slack_report.clear()
    report_reader.clear()
