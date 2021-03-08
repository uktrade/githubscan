

from github.report import Report

from django.conf import settings
from django.db.models import Sum
import json


class EmailReport(Report):

    def __init__(self):
        self.signature = settings.SIGNATURE
        super().__init__()

    def getReport(self):

        data = {}

        data.update(self.__format_email_report__(
            repositories_of_interest=self.getReportRepos()))
        data.update(
            {'subject': 'Daily : Github Organisation Vulnerabilities Scan Report'})
        data.update({'signature': self.signature})
        return data

    def getSkippedRepoReport(self):
        data = {}

        data.update(self.__format_email_report__(
            repositories_of_interest=self.getSkippedRepos()))
        data.update(
            {'subject': 'Daily : Github Organisation Unmonitored Repositories Vulnerabilities Scan Report'})
        data.update({'signature': self.signature})

        return data

    def getTeamReport(self, team):
        data = {}

        data.update(self.__format_email_report__(
            repositories_of_interest=self.getTeamReportRepos(team=team), teams=team))
        data.update(
            {'subject': f'Daily : Github {team.capitalize()} Team Vulnerabilities Scan Report'})
        data.update({'signature': self.signature})

        return data

    def __format_email_report__(self, repositories_of_interest, teams=None):

        content = ''
        summary = ''

        csv_data = list()

        csv_data.append(["repository", "teams", "Package",
                         "Severity", "type", "value", "URL", "Github URL","SLO Breach","publish_age_in_days","detection_age_in_days"])

        report_repositories = self.db_client.getSortedVunrableRepos(
            repositories=repositories_of_interest)

        for vulnerable_repository in report_repositories:
            repository = vulnerable_repository.repository.name
            repo_teams = None
            if teams == None:
                repo_teams = list(self.db_client.getRepoTeams(
                    repository=repository).values_list('name', flat=True))
                repo_teams = " | ".join(repo_teams)
            else:
                repo_teams = teams

            github_alerts_link = "https://github.com/uktrade/{}/network/alerts".format(
                repository)

            content += "#{}\n * Critical: {} \n * High: {}\n * Moderate: {}\n * Low:{}\n * Associated team(s): {}\n * GitHub link: {} \n \n".format(
                repository, vulnerable_repository.critical, vulnerable_repository.high, vulnerable_repository.moderate, vulnerable_repository.low, repo_teams, github_alerts_link)


            #Add SLO Breach count
            slo_breache_counts = self.db_client.getRepoSloBreach(repository=repository)
            if slo_breache_counts:
                    slo_breache_counts = slo_breache_counts[0]
                    content += "## SLO breach ##\n * Critical breach: {}\n * High breach: {}\n * Moderate breach: {}\n\n".format(slo_breache_counts.critical,slo_breache_counts.high,slo_breache_counts.moderate)

            #Get detailed report for csv
            repository_vulnerabilities = self.db_client.getDetailsRepoVulnerabilities(
                repository=repository)

            for vulnerability in repository_vulnerabilities:
                csv_data.append([repository, repo_teams, vulnerability.package_name, vulnerability.severity_level,
                                 vulnerability.identifier_type, vulnerability.identifier_value, vulnerability.advisory_url, github_alerts_link,
                                 vulnerability.slo_breach,vulnerability.publish_age_in_days,vulnerability.detection_age_in_days])

        #Vulnerability Summary
        summary += "#Vulnerability Summary\n * total Repositories: {}\n * total Critial: {}\n * total High: {}\n * total Moderate: {}\n * total Low: {}\n \n".format(
            report_repositories.count(),
            report_repositories.aggregate(sum=Sum('critical'))[
                'sum'], report_repositories.aggregate(sum=Sum('high'))['sum'],
            report_repositories.aggregate(sum=Sum('moderate'))['sum'], report_repositories.aggregate(sum=Sum('low'))['sum'])


        #SLO Breach Summary
        slo_breached_repositories_of_interest = set(self.db_client.getSloBreachRepos().values_list('repository',flat=True)).intersection(set(report_repositories.values_list('repository',flat=True)))

        slo_breached_report_repositories = self.db_client.getSloBreachReposOfInterest(repositories=slo_breached_repositories_of_interest)

        summary += "#SLO Breach Summary\n * total Repositories: {}\n * total Critial breach: {}\n * total High breach: {}\n * total Moderate breach: {}\n\n".format(
            slo_breached_report_repositories.count(),
            slo_breached_report_repositories.aggregate(sum=Sum('critical'))[
                'sum'], slo_breached_report_repositories.aggregate(sum=Sum('high'))['sum'],
            slo_breached_report_repositories.aggregate(sum=Sum('moderate'))['sum'])


        return {'csv': csv_data, 'content': content, 'summary': summary}
