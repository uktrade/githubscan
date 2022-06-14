# -*- coding: utf-8 -*-
def test_exception_1_slack_message_setter(build_slack_report, caplog):
    """Data is not a dict"""
    try:
        build_slack_report.slack_message = "string data"
        assert False
    except TypeError:
        assert "message_data expected to be dict type but is str" in caplog.messages
        assert True


def test_exception_2_slack_message_setter(build_slack_report):
    """no header key in dict"""
    try:
        build_slack_report.slack_message = {"key": "val", "section": "section_text"}
        assert False
    except KeyError:
        assert True


def test_exception_3_slack_message_setter(build_slack_report):
    """no section key in dict"""
    try:
        build_slack_report.slack_message = {"header": "header"}
        assert False
    except KeyError:
        assert True


def test_exception_4_slack_message_setter(build_slack_report, caplog):
    """section is not a list"""
    try:
        build_slack_report.slack_message = {
            "header": "header",
            "section": "section_text",
        }
        assert False
    except TypeError:
        assert (
            'message_data["section"] expected to be list type but is str'
            in caplog.messages
        )
        assert True


def test_slack_message_setter_simple(build_slack_report):
    header = "my header"
    section = ["text1", "text2"]

    build_slack_report.slack_message = {"header": header, "section": section.copy()}

    expected_message = [
        {
            "type": "header",
            "text": {"type": "plain_text", "text": header},
        },
        {
            "type": "section",
            "text": {"type": "mrkdwn", "text": "```" + "\n".join(section) + "\n```"},
        },
    ]

    assert build_slack_report.slack_message[0] == expected_message[0]
    assert build_slack_report.slack_message[1] == expected_message[1]

    build_slack_report.clear()


def test_slack_message_setter_length_more_than_limit(build_slack_report):

    header = "header text"
    section = [
        "this is first line",
        "this is second line",
        "this is third line",
        "this is forth line",
        "this is firth line",
        "this is sixth line",
    ]

    build_slack_report.max_message_length = 30
    build_slack_report.slack_message = {"header": header, "section": section.copy()}

    assert (len(build_slack_report.slack_message)) == 6

    build_slack_report.clear()
