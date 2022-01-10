

from github.report import Report

from django.conf import settings
from django.db.models import Sum
import json

from django.db.models import Case, When
from datetime import  datetime,timedelta
import calendar

class EmailReport(Report):

    def __init__(self):
        self.signature = settings.SIGNATURE
        super().__init__()

    def getReport(self):

        data = {}

        data.update(self.__format_email_report__(
            repositories_of_interest=self.getReportRepos()))
        data.update(
            {'subject': 'Daily: Github Organisation Vulnerabilities Scan Report'})
        data.update({'signature': self.signature})
        return data

    def getSkippedRepoReport(self):
        data = {}

        data.update(self.__format_email_report__(
            repositories_of_interest=self.getSkippedRepos()))
        data.update(
            {'subject': 'Daily: Github Organisation Unmonitored Repositories Vulnerabilities Scan Report'})
        data.update({'signature': self.signature})

        return data

    def getTeamReport(self, team):
        data = {}

        data.update(self.__format_email_report__(
            repositories_of_interest=self.getTeamReportRepos(team=team), teams=team))
        data.update(
            {'subject': f'Daily: Github {team.capitalize()} Team Vulnerabilities Scan Report'})
        data.update({'signature': self.signature})
      
        return data

    def getDetailedTeamReport(self,team):
        data = {}
        data.update(self.__detailed_repository_report(repositories_of_interest=self.getTeamReportRepos(team=team),team=team))
        data.update(
            {'subject': f"{data['subject_prefix']} - {team.capitalize()} Team Github Report"})
        data.update({'subject_prefix':''})
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
                repo_teams = list(
                    self.db_client.getRepoTeams(
                        repository=repository
                    ).values_list(
                        'name', flat=True
                    )
                )
                repo_teams = " | ".join(repo_teams)
            else:
                repo_teams = teams

            github_alerts_link = "https://github.com/uktrade/{}/network/alerts".format(
                repository)

            SLA_BREACH_TEXT = f"* Effective Critical Breach: {vulnerable_repository.effective_slabreach:3d}"
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

        # subject_prefix
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
        summary += f"#Report Rating\n {subject_prefix}\n #Vulnerability Summary\n * total Repositories: {report_repositories.count()}\n * total Effective Critical Breach: {report_repositories.aggregate(sum=Sum('effective_slabreach'))['sum']}\n * total Critical: {report_repositories.aggregate(sum=Sum('critical'))['sum']} --> Effective Critical: {report_repositories.aggregate(sum=Sum('effective_critical'))['sum']}\n * total High: {report_repositories.aggregate(sum=Sum('high'))['sum']} ---> Effective High: { report_repositories.aggregate(sum=Sum('effective_high'))['sum']}\n * total Moderate: { report_repositories.aggregate(sum=Sum('moderate'))['sum']} --> Effective Moderate: { report_repositories.aggregate(sum=Sum('effective_moderate'))['sum']}\n * total Low: { report_repositories.aggregate(sum=Sum('low'))['sum']} --> Effective Low: { report_repositories.aggregate(sum=Sum('effective_low'))['sum']}\n \n"

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

        return {'csv': csv_data, 'content': content, 'summary': summary, 'subject_prefix': f'[{subject_prefix}]'}



    def __detailed_repository_report(self,repositories_of_interest,team):

        max_critical_alert_age = 1
        max_high_alert_age = 7
        max_moderate_alert_age = 15
        time_since_current_level = 0

        content = ''
        
        vulnerabilities = self.db_client.getRepositoriesVulnerabilities(repositories=repositories_of_interest)

        sorted_uniq_vulnerabilities = vulnerabilities.values('package_name','severity_level','effective_severity_level','detection_age_in_days','time_since_current_level','advisory_url','patched_version').distinct().annotate(ranking = Case(When(severity_level='critical',then=1),When(severity_level='high',then=2),When(severity_level='moderate',then=3),When(severity_level='low',then=4)),
                        effective_ranking = Case(When(effective_severity_level='SLA_BREACH',then=1),When(effective_severity_level='critical',then=2),When(effective_severity_level='high',then=3),When(effective_severity_level='moderate',then=4),When(effective_severity_level='low',then=5))
                    ).order_by('effective_ranking','ranking')

        subject_prefix = ''
        vulnerable_package_count = sorted_uniq_vulnerabilities.count()

        for index,v in enumerate(sorted_uniq_vulnerabilities):

            package_name = v['package_name']
            patched_version = v['patched_version']
            severity_level = v['severity_level']
            current_severity_level = v['effective_severity_level'] or v['severity_level']

            time_in_hand = 0
            time_in_hand_suffix = 'days'

            time_since_key = f'Time Being {(current_severity_level).capitalize()}' 
            days_left_to_breach_key = f'Time Till {(current_severity_level).capitalize()} Breach'

            days_left_to_breach = ''
            advisory_url = v['advisory_url']

            repository_key = 'Repository'

            time_since_current_level = v['time_since_current_level']

            if current_severity_level == 'SLA_BREACH':
                current_severity_level = "Critical Breach"
                time_in_hand = -1
                time_in_hand_suffix = 'Breached Already'
                time_since_key = f"Time Since {current_severity_level}"
                days_left_to_breach_key = f"Time Till {(current_severity_level).capitalize()}"
                days_left_to_breach = f"{v.time_since_current_level} day(s) over SLA Budget"

            elif current_severity_level == 'critical':
                time_left = max_critical_alert_age - v['time_since_current_level']
                time_in_hand = time_left
                time_in_hand_suffix = 'day'
                days_left_to_breach = f'{time_left} days(s)'

            elif current_severity_level == 'high':
                time_left = max_high_alert_age - v['time_since_current_level']
                time_in_hand = time_left + max_critical_alert_age
                days_left_to_breach = f'{time_left} days(s)'

            elif current_severity_level == 'moderate':
                time_left = max_moderate_alert_age - v['time_since_current_level']
                time_in_hand = time_left + max_high_alert_age + max_critical_alert_age
                days_left_to_breach = f'{time_left} days(s)'                        

            elif current_severity_level == 'low':
                time_in_hand = 365;


            repositories = vulnerabilities.filter(package_name=v['package_name'],
                                                severity_level=v['severity_level'],
                                                effective_severity_level=v['effective_severity_level'],
                                                detection_age_in_days=v['detection_age_in_days'],
                                                time_since_current_level=v['time_since_current_level']).values('repository_id').distinct();

            
            if len(repositories) > 1:
               repository_key = 'Repositories'
            due_date = datetime.today() + timedelta(time_in_hand)

            due_day = due_date.day
            due_day_suffix = ''

            if 4 <= due_day <= 20 or 24 <= due_day <= 30:
                due_day_suffix = "th"
            else:
                due_day_suffix = ["st", "nd", "rd"][due_day % 10 - 1]

            due_month = calendar.month_name[due_date.month]
 
            if time_in_hand == 1:
                time_in_hand = 'Tomorrow'

            elif time_in_hand == 0:
                time_in_hand = 'Today'

            elif time_in_hand == -1:
                time_in_hand = 'Yesterday'

            elif time_in_hand < -1:
                time_in_hand = f'{abs(time_in_hand)} days ago'
                time_in_hand_suffix = ''
            else:
                time_in_hand = f'{time_in_hand} {time_in_hand_suffix}'            

        
            due_date_str = f'{due_day}{due_day_suffix} {due_month} {due_date.year} ({time_in_hand})'

            repo_urls = '' 


            for repo in repositories:
                repo_urls += f" - https://github.com/uktrade/{repo['repository_id']}/security/dependabot\n "
            
            content += f'#{package_name.capitalize()}\nPatch by: {due_date_str} \n * Patched version: {patched_version}\n * Effective severity: {current_severity_level.capitalize()}\n *Original severity: {severity_level.capitalize()} \n * Advisory: \n  - {advisory_url} \n * {repository_key}:\n {repo_urls}\n\n'

            if index == 0:

                subject_prefix = f'Action by: {due_day}{due_day_suffix} {due_month} {due_date.year}'
                if current_severity_level == 'SLA_BREACH':
                    subject_prefix = 'Critical Breach'


        return {'content': content,'csv':'','subject_prefix': f'[{subject_prefix}] {vulnerable_package_count} Vulnerable packages','summary':''}