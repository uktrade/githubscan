from github.report import Report

from django.db.models import Sum


class SlackReport(Report):

    def __init__(self):
        super().__init__()
        self.slack_message = []
        

    def getReportMessage(self):
        self.__getSummaryReport__()
        self.__getSkippedRepoReport__()
        self.__getSloBreachReport__()
        self.__getOrphanRepoReport__()
        return self.slack_message


    def __addHeaderAndSectionToBlock__(self,header,section_text):
        message_header = { "type": "header", "text": {"type":"plain_text","text": header } }
        message_section = { "type": "section", "text": {"type":"mrkdwn","text": section_text } }
        
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

        header = "GitHub Severity Report Summary"
        section_text = f"```Total Repositories: {total_repositories}\ntotal Critical: {total_critical}\ntotal High: {total_high}\ntotal Moderate: {total_moderate}\ntotal Low: {total_low}```"
        
        self.__addHeaderAndSectionToBlock__(header=header,section_text=section_text)

        #self.slack_message += f"```\nThis is the daily Github severity report summary.\nTotal Repositories: {total_repositories}\ntotal Critical: {total_critical}\ntotal High: {total_high}\ntotal Moderate: {total_moderate}\ntotal Low: {total_low}\n```\n"

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

        

        if total_repositories >= 1:

            total_header = "Github UNMONITORED Repos severity summary"

            total_section_text = f"```Total Repositories: {total_repositories}\ntotal Critical: {total_critical}\ntotal High: {total_high}\ntotal Moderate: {total_moderate}\ntotal Low: {total_low}```" 
        
            self.__addHeaderAndSectionToBlock__(header=total_header,section_text=total_section_text)


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

            self.__addHeaderAndSectionToBlock__(header=header,section_text=section_text)


    def __getSloBreachReport__(self):
        repositories = set((self.db_client.getRepos()).filter(
            skip_scan=False).values_list('name', flat=True))
        slo_breaching_repositories = set(
            self.db_client.getSloBreachRepos().values_list('repository', flat=True))

        repositories_of_interest = repositories.intersection(slo_breaching_repositories)

        report_repositories = self.db_client.getSloBreachReposOfInterest(repositories=repositories_of_interest)

        total_repositories = report_repositories.count()
        total_critical = report_repositories.aggregate(sum=Sum('critical'))[
            'sum']
        total_high = report_repositories.aggregate(sum=Sum('high'))['sum']
        total_moderate = report_repositories.aggregate(sum=Sum('moderate'))[
            'sum']
        
        if total_repositories >=1:
            total_header = "Github SLO Breach report summary"

            total_section_text = f"```Total Repositories: {total_repositories}\ntotal Critical: {total_critical}\ntotal High: {total_high}\ntotal Moderate: {total_moderate}```" 
        
            self.__addHeaderAndSectionToBlock__(header=total_header,section_text=total_section_text)

    def __getOrphanRepoReport__(self):
        all_repositories = set(self.db_client.getRepos().values_list('name',flat=True))
        
        repos_with_team = []
        for team in self.db_client.getTeams():
            if team.name != 'default':
                repos_with_team += list(set(team.repositories.values_list('name',flat=True)))

        orphan_repositories = all_repositories.difference(set(repos_with_team))

        if orphan_repositories:
            header = "Github Orphan repos report"
            section_text = f"```Total Orphan Repositories:{len(orphan_repositories)}\n"
            header_set = False
            for orphan_repo in orphan_repositories:
                if len(section_text) < 2800:
                    section_text += f"* <https://github.com/uktrade/{orphan_repo}/settings/access | {orphan_repo}>\n"

                else:
                    section_text += "```"
                    if not header_set:
                        self.__addHeaderAndSectionToBlock__(header=header,section_text=section_text)
                        header_set = True
                    else:
                        self.__addHeaderAndSectionToBlock__(header="-",section_text=section_text)                        
                    section_text = "```"