

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
                         "Severity", "type", "value", "URL", "Github URL", "SLO Breach", "publish_age_in_days", "detection_age_in_days"])

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

            SLA_BREACH_TEXT = f"* Critical Breach: {vulnerable_repository.effective_slabreach:3d}"
            CRITICAL_ALERT_TEXT = "{:12s} {:3d} --> {:20s} {:3d}".format(
                "* Critical:", vulnerable_repository.critical, "Effective Critical:", vulnerable_repository.effective_critical)
            HIGH_ALERT_TEXT = "{:12s} {:3d} --> {:20s} {:3d}".format(
                "* High:", vulnerable_repository.high, "Effective High:", vulnerable_repository.effective_high)
            MODERATE_ALERT_TEXT = "{:12s} {:3d} --> {:20s} {:3d}".format(
                "* Moderate:", vulnerable_repository.moderate, "Effective Moderate:", vulnerable_repository.effective_moderate)
            LOW_ALERT_TEXT = "{:12s} {:3d} --> {:20s} {:3d}".format(
                "* Low:", vulnerable_repository.low, "Effective Low:", vulnerable_repository.effective_low)
            ASSOCIATED_TEAMS_TEXT = f"* Associated team(s): {repo_teams}"
            GITHUB_LINK_TEXT = f"* GitHub link: {github_alerts_link}"

            content += f"#{repository}\n{SLA_BREACH_TEXT}\n{CRITICAL_ALERT_TEXT}\n{HIGH_ALERT_TEXT}\n{MODERATE_ALERT_TEXT}\n{LOW_ALERT_TEXT}\n{ASSOCIATED_TEAMS_TEXT}\n{GITHUB_LINK_TEXT}\n \n"

            # Add SLO Breach count
            slo_breache_counts = self.db_client.getRepoSloBreach(
                repository=repository)
            if slo_breache_counts:
                slo_breache_counts = slo_breache_counts[0]
                content += "## SLO breach ##\n * Critical breach: {}\n * High breach: {}\n * Moderate breach: {}\n\n".format(
                    slo_breache_counts.critical, slo_breache_counts.high, slo_breache_counts.moderate)

            # Get detailed report for csv
            repository_vulnerabilities = self.db_client.getDetailsRepoVulnerabilities(
                repository=repository)

            for vulnerability in repository_vulnerabilities:
                csv_data.append([repository, repo_teams, vulnerability.package_name, vulnerability.severity_level,
                                 vulnerability.identifier_type, vulnerability.identifier_value, vulnerability.advisory_url, github_alerts_link,
                                 vulnerability.slo_breach, vulnerability.publish_age_in_days, vulnerability.detection_age_in_days])


        #subject_prefix
        subject_prefix = 'GREEN'

        if report_repositories.aggregate(sum=Sum('effective_slabreach'))['sum']:
            subject_prefix = 'RED'

        else:
            if report_repositories.aggregate(sum=Sum('effective_critical'))['sum'] != report_repositories.aggregate(sum=Sum('critical'))['sum']:
                subject_prefix = 'AMBER'
            if report_repositories.aggregate(sum=Sum('effective_high'))['sum'] != report_repositories.aggregate(sum=Sum('high'))['sum']:
                subject_prefix = 'AMBER'
            if report_repositories.aggregate(sum=Sum('effective_moderate'))['sum'] != report_repositories.aggregate(sum=Sum('moderate'))['sum']:
                subject_prefix = 'AMBER'


        # Vulnerability Summary
        summary += f"#Report Rating\n {subject_prefix}\n #Vulnerability Summary\n * total Repositories: {report_repositories.count()}\n * total Critical Breach: {report_repositories.aggregate(sum=Sum('effective_slabreach'))['sum']}\n * total Critical: {report_repositories.aggregate(sum=Sum('critical'))['sum']} --> Effective Critical: {report_repositories.aggregate(sum=Sum('effective_critical'))['sum']}\n * total High: {report_repositories.aggregate(sum=Sum('high'))['sum']} ---> Effective High: { report_repositories.aggregate(sum=Sum('effective_high'))['sum']}\n * total Moderate: { report_repositories.aggregate(sum=Sum('moderate'))['sum']} --> Effective Moderate: { report_repositories.aggregate(sum=Sum('effective_moderate'))['sum']}\n * total Low: { report_repositories.aggregate(sum=Sum('low'))['sum']} --> Effective Low: { report_repositories.aggregate(sum=Sum('effective_low'))['sum']}\n \n"

        # SLO Breach Summary
        slo_breached_repositories_of_interest = set(self.db_client.getSloBreachRepos().values_list(
            'repository', flat=True)).intersection(set(report_repositories.values_list('repository', flat=True)))

        slo_breached_report_repositories = self.db_client.getSloBreachReposOfInterest(
            repositories=slo_breached_repositories_of_interest)

        summary += "#SLO Breach Summary\n * total Repositories: {}\n * total Critical breach: {}\n * total High breach: {}\n * total Moderate breach: {}\n\n".format(
            slo_breached_report_repositories.count(),
            slo_breached_report_repositories.aggregate(sum=Sum('critical'))[
                'sum'], slo_breached_report_repositories.aggregate(sum=Sum('high'))['sum'],
            slo_breached_report_repositories.aggregate(sum=Sum('moderate'))['sum'])


        return {'csv': csv_data, 'content': content, 'summary': summary,'subject_prefix': f'[{subject_prefix}]'}
