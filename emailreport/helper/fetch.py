from github.helper.fetch.Db import Data
from github.helper.fetch.Github import Info as githubClient
from random import choice


class Report:

    def __init__(self):
        self.dbData = Data()
        self.gc = githubClient()

    def getReport(self):
        report = dict()
        for repo in self.dbData.getVulnerableRepos():
            teams = list(self.dbData.getRepoteams(
                repository=repo).values_list('team', flat=True))
            report[repo] = {
                'teams': teams, 'severities': self.gc.getVulnerabilityDetails(repository=repo)}

        return report
