

from github.report import Report

from django.conf import settings
from django.db.models import Sum
import json

class EmailReport(Report):

    def __init__(self):
        self.signature = json.loads(settings.SIGNATURE)
        super().__init__()

    def getReport(self):

        data = {}

        data.update(self.__format_email_report__(repositories_of_interest=self.getReportRepos()))
        data.update({'subject': 'Daily : Github Organisation Vulnerabilities Scan Report'})
        data.update({'signature': self.signature})    
        return data
       
    def getSkippedRepoReport(self):
        data = {}

        data.update(self.__format_email_report__(repositories_of_interest=self.getSkippedRepos()))
        data.update({'subject': 'Daily : Github Organisation Unmonitored Repositories Vulnerabilities Scan Report'})
        data.update({'signature': self.signature})    

        return data

    def getTeamReport(self,team):
        data = {}
     
        data.update(self.__format_email_report__(repositories_of_interest=self.getTeamReportRepos(team=team),teams=team))
        data.update({'subject': f'Daily : Github {team.capitalize()} Team Vulnerabilities Scan Report'})
        data.update({'signature': self.signature})    

        return data

    def __format_email_report__(self,repositories_of_interest,teams=None):

        content = ''
        summary = ''

        csv_data = list()
        
        csv_data.append(["repository", "teams", "Package","Severity", "type", "value", "URL", "Github URL"])

        report_repositories = self.db_client.getSortedVunrableRepos(repositories=repositories_of_interest)
 
        for vulnerable_repository in report_repositories:
            repository = vulnerable_repository.repository.name
            repo_teams = None
            if teams == None:
                repo_teams = list(self.db_client.getRepoTeams(repository=repository).values_list('team',flat=True))
                repo_teams = " | ".join(repo_teams)
            else:
                repo_teams = teams

            github_alerts_link = "https://github.com/uktrade/{}/network/alerts".format(repository)

            content += "#{}\n * Critical: {} \n * High: {}\n * Moderate: {}\n * Low:{}\n * Associated team(s): {}\n * GitHub link: {} \n \n".format(
                        repository, vulnerable_repository.critical,vulnerable_repository.high,vulnerable_repository.moderate,vulnerable_repository.low,repo_teams, github_alerts_link)


            repository_vulnerabilities = self.db_client.getDetailsRepoVulnerabilities(repository=repository)

            for vulnerability in repository_vulnerabilities:
                csv_data.append([repository,repo_teams,vulnerability.package_name,vulnerability.severity_level,vulnerability.identifier_type,vulnerability.identifier_value,vulnerability.advisory_url,github_alerts_link])
        
        summary += "#Summary\n * total Repositories: {}\n * total Critial: {}\n * total High: {}\n * total Moderate: {}\n * total Low: {}\n \n".format(
            report_repositories.count(),
            report_repositories.aggregate(sum=Sum('critical'))['sum'],report_repositories.aggregate(sum=Sum('high'))['sum'],
            report_repositories.aggregate(sum=Sum('moderate'))['sum'],report_repositories.aggregate(sum=Sum('low'))['sum'])

        return {'csv': csv_data,'content': content , 'summary': summary}