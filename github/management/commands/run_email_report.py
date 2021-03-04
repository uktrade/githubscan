from github.report.email import EmailReport

from notifications_python_client.notifications import NotificationsAPIClient
from notifications_python_client import prepare_upload
from django.conf import settings


from django.core.management.base import BaseCommand
from django.conf import settings

import os
import csv
import json
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.email_org_report()
        self.email_team_reports()

    def email_org_report(self):
        try:
            report = EmailReport()
            data =report.getReport()
            emails = settings.ORG_REPORT_EMAILS
            self.__send_email__(emails,data)
            self.stdout.write(self.style.SUCCESS(
                "Org Email Sent to: {}".format(",".join(emails))))
        except Exception as e:
            print("Org  Email Send Error:{}".format(e))
            traceback.print_exc()
    
    def email_team_reports(self):
        try:
            report = EmailReport()
            teams_emails = json.loads(settings.TEAMS_REPORT_EMAILS)
            for team,emails in teams_emails.items():
                data =report.getTeamReport(team=team)
                if data['content']:
                    self.__send_email__(emails,data)
                    self.stdout.write(self.style.SUCCESS(
                         "Team Email Sent to: {}".format(",".join(emails))))
        except Exception as e:
            print("Org  Email Send Error:{}".format(e))
            traceback.print_exc()
    

    def __send_email__(self, emails,data):
        notifications_client = NotificationsAPIClient(settings.NOTIFY_API_KEY)

        FILE_NAME = 'report.csv'

        with open(FILE_NAME, 'w') as csvFile:
            f = csv.writer(csvFile)
            f.writerows(data['csv'])
            csvFile.close()

        for to in emails:
            with open(FILE_NAME, 'rb') as f:
                response = notifications_client.send_email_notification(
                    email_address=to,
                    template_id=settings.NOTIFY_TEMPLATE_ID,
                    personalisation={
                        'subject': data['subject'],
                        'content': data['content'],
                        'summary': data['summary'],
                        'report': prepare_upload(f),
                        'signature': data['signature']
                    }
                )

        os.remove(FILE_NAME)