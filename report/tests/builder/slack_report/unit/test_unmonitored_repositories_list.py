# -*- coding: utf-8 -*-
import re


def test_unmonitored_repositories_list(
    build_slack_report, report_reader, data_index, processed_data
):

    report_reader.load_data_from_dict = processed_data

    build_slack_report.unmonitored_repositories_list(report_reader=report_reader)

    assert (
        build_slack_report.slack_message[0]["text"]["text"]
        == "Github Unmonitored Repositories list"
    )

    TOTAL_REPOSITORY_TEXT = f'{"Total Repositories:":20s}'

    assert re.search(
        f"{TOTAL_REPOSITORY_TEXT}{3:3d}",
        build_slack_report.slack_message[1]["text"]["text"],
    )

    build_slack_report.clear()
    report_reader.clear()
