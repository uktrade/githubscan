# -*- coding: utf-8 -*-
def test_exception_1__add_slack_headr_and_message(build_slack_report, caplog):
    """
    Header is incorrect type
    """
    header = 10
    section_text = "string"

    try:
        build_slack_report._add_slack_headr_and_message(
            header=header, section_text=section_text
        )
        assert False
    except TypeError:
        assert "header expected to be str type but is int" in caplog.messages
        assert True


def test_exception_2__add_slack_headr_and_message(build_slack_report, caplog):
    """
    section_text value is incorrect type
    """
    header = "header"
    section_text = ["string"]

    try:
        build_slack_report._add_slack_headr_and_message(
            header=header, section_text=section_text
        )
        assert False
    except TypeError:
        assert "section_text expected to be str type but is list" in caplog.messages
        assert True


def test__add_slack_headr_and_message(build_slack_report):
    """
    both value are correct
    """
    header = "header_text"
    section_text = "section text"

    expected_slack_message = [
        {"type": "header", "text": {"type": "plain_text", "text": header}},
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": section_text},
        },
    ]

    try:
        build_slack_report._add_slack_headr_and_message(
            header=header, section_text=section_text
        )
        assert build_slack_report.slack_message[0] == expected_slack_message[0]
        assert build_slack_report.slack_message[1] == expected_slack_message[1]
        assert True
    except TypeError:
        assert False

    build_slack_report.clear()
