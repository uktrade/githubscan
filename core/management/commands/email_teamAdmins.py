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
            teams = set(dbData.getTeamsFromAdminTable())

            for team in teams:
                admin_email = dbData.getTeamAdminEmail(team=team)
                if(admin_email):
                    report = Report()
                    process_report = ReportData()
                    data = process_report.format(
                        raw_report=report.getTeamReport(team=team))

                    if (data):
                        Email([admin_email], data)

        except Exception as e:
            print("Team Email Send Error:{}".format(e))
            traceback.print_exc()
