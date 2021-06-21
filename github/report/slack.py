from github.report import Report
from django.db.models import Sum

class SlackReport(Report):

    def __init__(self):
        super().__init__()
        self.slack_message = []

    def getReportMessage(self):
        self.__getSummaryReport__()
        self.__getTeamSummaryReport__()
        self.__getSkippedRepoReport__()
        self.__getSloBreachReport__()
        self.__getOrphanRepoReport__()

        return self.slack_message

    def __addHeaderAndSectionToBlock__(self, header, section_text, fields_array=[]):
        message_header = {"type": "header", "text": {
            "type": "plain_text", "text": header}}

        message_section = {}
        if fields_array:
            message_section.update(
                {"type": "section", "fields": fields_array[:10]})

        else:
            message_section.update(
                {"type": "section", "text": {"type": "mrkdwn", "text": section_text}})

        self.slack_message.append(message_header)
        self.slack_message.append(message_section)

    def __getSummaryReport__(self):

        repositories_of_interest = self.getReportRepos()
        report_repositories = self.db_client.getSortedVunrableRepos(
            repositories=repositories_of_interest)
        total_repositories = report_repositories.count()

        total_critical = report_repositories.aggregate(sum=Sum('critical'))[
            'sum']
        total_high = report_repositories.aggregate(sum=Sum('high'))['sum']
        total_moderate = report_repositories.aggregate(sum=Sum('moderate'))[
            'sum']
        total_low = report_repositories.aggregate(sum=Sum('low'))['sum']

        total_effective_slabreach = report_repositories.aggregate(sum=Sum('effective_slabreach'))[
            'sum']
        total_effective_critical = report_repositories.aggregate(sum=Sum('effective_critical'))[
            'sum']
        total_effective_high = report_repositories.aggregate(
            sum=Sum('effective_high'))['sum']

        total_effective_moderate = report_repositories.aggregate(
            sum=Sum('effective_moderate'))['sum']

        total_effective_low = report_repositories.aggregate(
            sum=Sum('effective_low'))['sum']

        header = "GitHub Severity Report Summary"
        section_text = f"```Total Repositories: {total_repositories}\nTotal Effective Critical Breach: {total_effective_slabreach}\ntotal Critical: {total_critical} --> Effective Critical: {total_effective_critical}\ntotal High: {total_high} --> Effective High: {total_effective_high} \ntotal Moderate: {total_moderate} --> Efeective Moderate: {total_effective_moderate}\ntotal Low: {total_low} --> Effective Low: {total_effective_low}```"

        self.__addHeaderAndSectionToBlock__(
            header=header, section_text=section_text)

    def __getTeamSummaryReport__(self):

        teams_summary_report = self.db_client.getSortedTeamsVulnerabilitySummaryReport()

        teams_report = []

        for report in teams_summary_report:
            teams_report.append(
                {report.team.name: f'[{report.critical},{report.high},{report.moderate},{report.low}] --> [{report.effective_slabreach},{report.effective_critical},{report.effective_high},{report.effective_moderate},{report.effective_low}]'})

        header = "GitHub Teams Severity Report Summary"
        section_text = f"```Total teams: {len(teams_report)}\n\n"

        if teams_report:
            for report in teams_report:
                if len(section_text) <= 2800:
                    for key, value in report.items():
                        section_text += f"{key}: {value}\n"
                else:
                    section_text += "```"
                    self.__addHeaderAndSectionToBlock__(
                        header=header, section_text=section_text)
                    header = "-"
                    section_text = "```"

        if len(section_text) >= 4:
            section_text += "```"
            self.__addHeaderAndSectionToBlock__(
                header=header, section_text=section_text)

    def __getSkippedRepoReport__(self):
        repositories_of_interest = self.getSkippedRepos()
        report_repositories = self.db_client.getSortedVunrableRepos(
            repositories=repositories_of_interest)

        total_repositories = report_repositories.count()
        total_critical = report_repositories.aggregate(sum=Sum('critical'))[
            'sum']
        total_high = report_repositories.aggregate(sum=Sum('high'))['sum']
        total_moderate = report_repositories.aggregate(sum=Sum('moderate'))[
            'sum']
        total_low = report_repositories.aggregate(sum=Sum('low'))['sum']

        total_header = "Github UNMONITORED Repos severity summary"

        if total_repositories <= 0:
            total_section_text = "None"
        else:
            total_section_text = f"```Total Repositories: {total_repositories}\ntotal Critical: {total_critical}\ntotal High: {total_high}\ntotal Moderate: {total_moderate}\ntotal Low: {total_low}```"

        self.__addHeaderAndSectionToBlock__(
            header=total_header, section_text=total_section_text)

        if total_repositories >= 1:

            header = "Github UNMONITORED Repos report"
            section_text = ""
            for vulnerable_repository in report_repositories:
                repository = vulnerable_repository.repository.name
                repo_teams = list(self.db_client.getRepoTeams(
                    repository=repository).values_list('team', flat=True))
                repo_teams = " | ".join(repo_teams)

                github_alerts_link = f"https://github.com/uktrade/{repository}/network/alerts"

                section_text += "```{}\nCritical: {}\nHigh: {}\nModerate: {}\nLow:{}\nAssociated team(s): {}\nGitHub link: {}\n\n".format(
                    repository,
                    vulnerable_repository.critical,
                    vulnerable_repository.high,
                    vulnerable_repository.moderate,
                    vulnerable_repository.low,
                    repo_teams,
                    github_alerts_link
                )

            section_text += "```\n"

            self.__addHeaderAndSectionToBlock__(
                header=header, section_text=section_text)

    def __getSloBreachReport__(self):
        repositories = set((self.db_client.getRepos()).filter(
            skip_scan=False).values_list('name', flat=True))
        slo_breaching_repositories = set(
            self.db_client.getSloBreachRepos().values_list('repository', flat=True))

        repositories_of_interest = repositories.intersection(
            slo_breaching_repositories)

        report_repositories = self.db_client.getSloBreachReposOfInterest(
            repositories=repositories_of_interest)

        total_repositories = report_repositories.count()
        total_critical = report_repositories.aggregate(sum=Sum('critical'))[
            'sum']
        total_high = report_repositories.aggregate(sum=Sum('high'))['sum']
        total_moderate = report_repositories.aggregate(sum=Sum('moderate'))[
            'sum']

        total_header = "Github SLO Breach report summary"

        total_section_text = f"```Total Repositories: {total_repositories}\ntotal Critical: {total_critical}\ntotal High: {total_high}\ntotal Moderate: {total_moderate}```"

        self.__addHeaderAndSectionToBlock__(
            header=total_header, section_text=total_section_text)

    def __getOrphanRepoReport__(self):
        all_repositories = set(
            self.db_client.getRepos().values_list('name', flat=True))

        repos_with_team = []
        for team in self.db_client.getTeams():
            if team.name != 'default':
                repos_with_team += list(
                    set(team.repositories.values_list('name', flat=True)))

        orphan_repositories = all_repositories.difference(set(repos_with_team))

        header = "Github Orphan repos report"
        section_text = f"```Total Orphan Repositories:{len(orphan_repositories)}\n"

        if orphan_repositories:
            for orphan_repo in orphan_repositories:
                if len(section_text) <= 2800:
                    section_text += f"* <https://github.com/uktrade/{orphan_repo}/settings/access | {orphan_repo}>\n"

                else:
                    section_text += "```"
                    self.__addHeaderAndSectionToBlock__(
                        header=header, section_text=section_text)
                    header = "-"
                    section_text = "```"

        if len(section_text) >= 4:
            section_text += "```"
            self.__addHeaderAndSectionToBlock__(
                header=header, section_text=section_text)
