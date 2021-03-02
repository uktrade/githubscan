from github.report import Report

from django.db.models import Sum

class SlackReport(Report):


    def __init__(self):
        super().__init__()
        self.slack_message = ""


    def getReportMessage(self):
        self.__getSummaryReport__()
        self.__getSkippedRepoReport__()
        return self.slack_message

    def __getSummaryReport__(self):

        repositories_of_interest=self.getReportRepos()
        report_repositories = self.db_client.getSortedVunrableRepos(repositories=repositories_of_interest)
        total_repositories = report_repositories.count()
        total_critical = report_repositories.aggregate(sum=Sum('critical'))['sum']
        total_high = report_repositories.aggregate(sum=Sum('high'))['sum']
        total_moderate = report_repositories.aggregate(sum=Sum('moderate'))['sum']
        total_low = report_repositories.aggregate(sum=Sum('low'))['sum']

        self.slack_message += f"```\nThis is the daily Github severity report summary.\nTotal Repositories: {total_repositories}\ntotal Critical: {total_critical}\ntotal High: {total_high}\ntotal Moderate: {total_moderate}\ntotal Low: {total_low}\n```\n"

        
    def __getSkippedRepoReport__(self):
        repositories_of_interest=self.getSkippedRepos()
        report_repositories = self.db_client.getSortedVunrableRepos(repositories=repositories_of_interest)

        total_repositories = report_repositories.count()
        total_critical = report_repositories.aggregate(sum=Sum('critical'))['sum']
        total_high = report_repositories.aggregate(sum=Sum('high'))['sum']
        total_moderate = report_repositories.aggregate(sum=Sum('moderate'))['sum']
        total_low = report_repositories.aggregate(sum=Sum('low'))['sum']

        self.slack_message += "```\nThis is the daily Github UNMONITORED Repos severity report summary."

        if total_repositories == 0:
            self.slack_message += "\nnothing to see here move on!\n```\n"

        else:    
            self.slack_message += f"\nTotal Repositories: {total_repositories}\ntotal Critical: {total_critical}\ntotal High: {total_high}\ntotal Moderate: {total_moderate}\ntotal Low: {total_low}\n```\n"

            self.slack_message += f"```\nThis is the daily Github UNMONITORED Repos report\n"

            for vulnerable_repository in report_repositories:
                repository = vulnerable_repository.repository.name
                repo_teams = list(self.db_client.getRepoTeams(repository=repository).values_list('team',flat=True))
                repo_teams = " | ".join(repo_teams)
                
                github_alerts_link = f"https://github.com/uktrade/{repository}/network/alerts"

                self.slack_message += "{}\nCritical: {}\nHigh: {}\nModerate: {}\nLow:{}\nAssociated team(s): {}\nGitHub link: {}\n\n".format(
                    repository,
                    vulnerable_repository.critical,
                    vulnerable_repository.high,
                    vulnerable_repository.moderate,
                    vulnerable_repository.low,
                    repo_teams,
                    github_alerts_link
                )

            self.slack_message +="```\n"