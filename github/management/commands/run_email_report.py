from github.report.email import EmailReport

from notifications_python_client.notifications import NotificationsAPIClient
from notifications_python_client import prepare_upload
from django.conf import settings


from django.core.management.base import BaseCommand
from django.conf import settings

from github.models import OrganisationNotificationTarget
from github.models import Team
from github.models import TeamNotificationTarget

import os
import csv
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.email_org_report()
        self.email_team_reports()
        self.email_detailed_team_reports()

    def email_org_report(self):
        try:
            report = EmailReport()
            data = report.getReport()
            emails = [
                obj.email
                for obj in OrganisationNotificationTarget.objects.all()
            ]
            self.__send_email__(emails, data, settings.NOTIFY_TEMPLATE_ID)
            self.stdout.write(self.style.SUCCESS(
                "Org Email Sent to: {}".format(",".join(emails)))
            )
        except Exception as e:
            print("Org  Email Send Error:{}".format(e))
            traceback.print_exc()

    def email_team_reports(self):
        """ Send team report to those teams configured with a notification
        target. Teams that have no actively vulnerable repos will only
        received notifications to targets that wish to receive all alerts -
        "RED" and "GREEN".
        """
        report = EmailReport()
        for team in Team.objects.filter(reporting_enabled=True):
            try:
                notification_targets = TeamNotificationTarget.objects.filter(
                    team=team
                )
                if not notification_targets:
                    self.stdout.write(self.style.NOTICE(
                        f'Team Report: Unable to notify "{team.name}" - no '
                        f'associated TeamNotificationTarget instances.'
                    ))
                    continue

                data = report.getTeamReport(team=team.name)
                if data['vulnerable_repo_count'] == 0:
                    # No vulnerable repos, so only notify those teams who want
                    # to be notified of "GREEN" alerts (as well as those that
                    # are "RED").
                    notification_targets = notification_targets.filter(
                        red_alerts_only=False
                    )
                emails = [obj.email for obj in notification_targets]
                if not emails:
                    continue

                self.__send_email__(emails, data, settings.NOTIFY_TEMPLATE_ID)
                self.stdout.write(self.style.SUCCESS(
                    "Team Email Sent to: {}".format(",".join(emails))
                ))
            except Exception as e:
                traceback.print_exc()

    def email_detailed_team_reports(self):
        """ Send detailed team report to those teams configured with a
        notification target and which have vulnerable repos.
        """
        report = EmailReport()
        for team in Team.objects.filter(reporting_enabled=True):
            try:
                notification_targets = TeamNotificationTarget.objects.filter(
                    team=team
                )
                if not notification_targets:
                    self.stdout.write(self.style.NOTICE(
                        f'Detailed Team Report: Unable to notify "{team.name}" '
                        f'- no associated TeamNotificationTarget instances.'
                    ))
                    continue

                data = report.getDetailedTeamReport(team=team.name)
                emails = [obj.email for obj in notification_targets]
                if data['content'] and emails:
                    self.__send_email__(
                        emails,
                        data,
                        settings.NOTIFY_DETAILED_VULNURABILITY_TEMPLATE_ID
                    )
                    self.stdout.write(self.style.SUCCESS(
                        f"Detailed Team[{team.name}] Report Email Sent to: {''.join(emails)}"
                    ))
            except Exception as e:
                print(f"Detailed Team[{team.name}] Report Send Error:{e}")
                traceback.print_exc()            

    def __send_email__(self, emails, data,notify_template_id):
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
            personalisation_data={
                    'subject': f"{data['subject_prefix']} {data['subject']}",
                    'content': data['content'],
                    'summary': data['summary'],
                    'report': upload_file,
                    'signature': data['signature']
            }            
            response = notifications_client.send_email_notification(
                email_address=to,
                template_id=notify_template_id,
                personalisation=personalisation_data
            )

        os.remove(FILE_NAME)