from github.report.slack import SlackReport

from django.conf import settings

from django.core.management.base import BaseCommand
from django.conf import settings

import traceback
import requests
import json


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            report = SlackReport()
            slack_message = report.getReportMessage()

            if settings.SLACK_ENABLED == 'True':
                url = f'{settings.SLACK_URL}/api/chat.postMessage'
                data = {'channel': f'{settings.SLACK_CHANNEL}',
                        'blocks': slack_message}
                headers = {'Content-type': 'application/json; charset=utf-8',
                           'Authorization': f'Bearer {settings.SLACK_TOKEN}'}
                response = requests.post(
                    url, data=json.dumps(data), headers=headers)
                slack_response = response.json()

                if not slack_response['ok']:
                    raise Exception(slack_response)

        except Exception as e:
            print("Core slack notification error:{}".format(e))
            traceback.print_exc()
