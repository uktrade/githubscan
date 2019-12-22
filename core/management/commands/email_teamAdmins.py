import traceback
from django.core.management.base import BaseCommand
from emailreport.helper.fetch import Report
from emailreport.helper.format import ReportData
from emailreport.helper.send import Email
from github.helper.fetch.Db import Data


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            dbData = Data()
            admin_emails = dbData.getTeamAdminEmails()
            for email in admin_emails:
                teams = dbData.getTeamsByAdminEmail(admin_email=email['admin_email'])

                report = Report()
                process_report = ReportData()
                raw_reports = {}

                for team in teams:
                    raw_reports.update(report.getTeamReport(team=team.name))
                    
                data = process_report.format(raw_report=raw_reports)
                if (data):
                    Email([team.admin_email], data)

        except Exception as e:
            print("Team Email Send Error:{}".format(e))
            traceback.print_exc()
