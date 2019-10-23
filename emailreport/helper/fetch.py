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

    def getTeamReport(self, team):
        report = dict()
        teamRepos = set(self.dbData.getTeamRepos(
            team=team).values_list('repository', flat=True))
        vulnerableRepos = set(self.dbData.getVulnerableRepos())

        vulnerableTeamRepos = teamRepos.intersection(vulnerableRepos)

        if (vulnerableTeamRepos):
            for repo in vulnerableTeamRepos:
                report[repo] = {
                    'teams': [team], 'severities': self.gc.getVulnerabilityDetails(repository=repo)}

        return report
