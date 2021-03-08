from github.db.retriver import Retriver


class Report:

    def __init__(self):
        self.db_client = Retriver()

    def getReportRepos(self):
        repositories = set((self.db_client.getRepos()).filter(
            skip_scan=False).values_list('name', flat=True))
        reported_repositories = set(
            self.db_client.getVulnerableRepositories().values_list('repository', flat=True))
        return repositories.intersection(reported_repositories)

    def getSkippedRepos(self):
        repositories = set((self.db_client.getRepos()).filter(
            skip_scan=True).values_list('name', flat=True))
        reported_repositories = set(
            self.db_client.getVulnerableRepositories().values_list('repository', flat=True))
        return repositories.intersection(reported_repositories)

    def getTeamReportRepos(self, team):
        team_repositories = set(self.db_client.getTeamRepos(
            team=team).repositories.values_list('name', flat=True))
        repositories = set((self.db_client.getRepos()).filter(
            skip_scan=False).values_list('name', flat=True))
        reported_repositories = set(
            self.db_client.getVulnerableRepositories().values_list('repository', flat=True))
        return (repositories.intersection(reported_repositories)).intersection(team_repositories)
