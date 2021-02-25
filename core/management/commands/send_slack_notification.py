import traceback
import requests
import json
from django.core.management.base import BaseCommand
from emailreport.helper.fetch import Report
from django.conf import settings
from collections import Counter

class Command(BaseCommand):

    def handle(self, *args, **options):
        try:

            report = Report()
            raw_report = report.getReport()
            severity_counter = Counter()

            for repository in raw_report.keys():

                severities = raw_report[repository]['severities']

                for severity in severities:
                    severity_counter[severity[1]] +=1

            slack_message = "```\nThis is the daily Github severity report.\nCritical: {}\nHigh: {}\nModerate: {}\nLow:{}\n```".format(
                severity_counter['critical'], severity_counter['high'], severity_counter['moderate'], severity_counter['low'])
            if settings.SLACK_ENABLED == 'True':
                print("Sending results to slack")
                url = f'{settings.SLACK_URL}/api/chat.postMessage'
                data = {'channel': f'{settings.SLACK_CHANNEL}', 'text': slack_message}
                headers = {'Content-type': 'application/json; charset=utf-8',
                'Authorization': f'Bearer {settings.SLACK_TOKEN}'}
                response = requests.post(url, data=json.dumps(data), headers=headers)
                slack_response = response.json()
                print(slack_response)                    

        except Exception as e:
            print("Core slack notification error:{}".format(e))
            traceback.print_exc()