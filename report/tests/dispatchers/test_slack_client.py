# -*- coding: utf-8 -*-
from django.conf import settings
import json

message = [
    {
        "type": "header",
        "text": {"type": "plain_text", "text": "Github Scan test"},
    },
    {
        "type": "section",
        "text": {"type": "mrkdwn", "text": "This is Github Scan Slack Test"},
    },
]


def test_slack_client_message_without_auth(real_fast_test, slack_dispatcher, caplog):
    try:
        global message

        slack_dispatcher.url = settings.SLACK_URL
        slack_dispatcher.auth_header = slack_dispatcher.bearer_auth_header

        data = json.dumps({"channel": settings.SLACK_CHANNEL, "blocks": message})
        slack_dispatcher.post_query = data

        slack_dispatcher.clear()
        assert False
    except:
        assert "Error: not_authed" in caplog.messages
        assert True


def test_slack_client_message(real_fast_test, slack_dispatcher):
    try:
        global message

        slack_dispatcher.url = settings.SLACK_URL
        slack_dispatcher.auth_header = slack_dispatcher.bearer_auth_header
        slack_dispatcher.auth_token = settings.SLACK_AUTH_TOKEN

        data = json.dumps({"channel": settings.SLACK_CHANNEL, "blocks": message})
        slack_dispatcher.post_query = data
        slack_dispatcher.clear()
        assert True
    except:
        assert False
