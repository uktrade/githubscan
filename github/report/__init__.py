from github.db.retriver import Retriver

class Report:

    def __init__(self):
        self.db_client = Retriver()

    def getReportRepos(self):
        repositories = set((self.db_client.getRepos()).filter(skip_scan=False).values_list('name',flat=True))
        reported_respositories = set(self.db_client.getVulnerableRepositories().values_list('repository',flat=True))
        return repositories.intersection(reported_respositories)

    def getSkippedRepos(self):
        repositories = set((self.db_client.getRepos()).filter(skip_scan=True).values_list('name',flat=True))
        reported_respositories = set(self.db_client.getVulnerableRepositories().values_list('repository',flat=True))
        return repositories.intersection(reported_respositories)


    def getTeamReportRepos(self,team):
        team_repositories = set(self.db_client.getTeamRepos(team=team).values_list('repository',flat=True))
        repositories = set((self.db_client.getRepos()).filter(skip_scan=False).values_list('name',flat=True))
        reported_respositories = set(self.db_client.getVulnerableRepositories().values_list('repository',flat=True))
        return (repositories.intersection(reported_respositories)).intersection(team_repositories)