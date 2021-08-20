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
        #self.email_org_report()
        self.email_team_reports()
        self.email_detailed_team_reports()

    def email_org_report(self):
        try:
            report = EmailReport()
            data = report.getReport()
            emails = settings.ORG_REPORT_EMAILS
            self.__send_email__(emails, data)
            self.stdout.write(self.style.SUCCESS(
                "Org Email Sent to: {}".format(",".join(emails))))
        except Exception as e:
            print("Org  Email Send Error:{}".format(e))
            traceback.print_exc()

    def email_team_reports(self):
        try:
            report = EmailReport()

            teams_emails = json.loads(
                settings.TEAMS_REPORT_EMAILS.replace('=>', ':'))
            for team, emails in teams_emails.items():
                data = report.getTeamReport(team=team)
                if data['content'] and emails:
                    self.__send_email__(emails, data)
                    self.stdout.write(self.style.SUCCESS(
                        "Team Email Sent to: {}".format(",".join(emails))))
        except Exception as e:
            print("Team  Email Send Error:{}".format(e))
            traceback.print_exc()

    def email_detailed_team_reports(self):
        report = EmailReport()
        teams_emails = json.loads(settings.TEAMS_REPORT_EMAILS.replace('=>', ':'))
        for team, emails in teams_emails.items():
            try:
                data = report.getDetailedTeamReport(team=team)
                if data['content'] and emails:
                    self.__send_email__(emails, data)
                    self.stdout.write(self.style.SUCCESS(f"Detailed Team[{team}] Report Email Sent to: {''.join(emails)}"))

            except Exception as e:
                print(f"Detailed Team[{team}] Report Send Error:{e}")
                traceback.print_exc()            

    def __send_email__(self, emails, data):
        notifications_client = NotificationsAPIClient(settings.NOTIFY_API_KEY)
    
        FILE_NAME = 'report.csv'

        with open(FILE_NAME, 'w') as csvFile:
            f = csv.writer(csvFile)
            f.writerows(data['csv'])
            csvFile.close()

        upload_file = ''

        if data['csv']:
            with open(FILE_NAME, 'rb') as f:
                upload_file = prepare_upload(f,is_csv=True) 

        for to in emails:
            response = notifications_client.send_email_notification(
                email_address=to,
                template_id=settings.NOTIFY_TEMPLATE_ID,
                personalisation={
                    'subject': f"{data['subject_prefix']} {data['subject']}",
                    'content': data['content'],
                    'summary': data['summary'],
                    'report': upload_file,
                    'signature': data['signature']
                }
            )

        os.remove(FILE_NAME)