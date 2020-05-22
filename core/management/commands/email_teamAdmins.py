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


                report_data = {}
                for team in teams:
                    if (team.admin_email):
                        admin_emails = team.admin_email.split(',')
                        report = Report()
                        team_report = report.getTeamReport(team=team.name)
        
                        report_data = self.merge_reports(report_data,team_report)                     
                        
            
                if(report_data):
                    process_report = ReportData()
                    data = process_report.format(raw_report=report_data)
                
                    Email(admin_emails, data)

        except Exception as e:
            print("Team Email Send Error:{}".format(e))
            traceback.print_exc()
            
            
    def merge_reports(self,report_data={},team_report={}):
        report_repos = set(report_data.keys())
        team_report_repos = set(team_report.keys())

        existing_repos = report_repos.intersection(team_report_repos)
        new_repos = team_report_repos.difference(report_repos)


        for repo in new_repos:
            report_data[repo] = team_report[repo]

        for repo in existing_repos:
            report_data[repo]['teams'] +=  team_report[repo]['teams']

        return report_data

