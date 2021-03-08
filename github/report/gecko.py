

from github.report import Report
from django.conf import settings
import json


class GeskoReport(Report):

    def __init__(self):
        super().__init__()

    def getReport(self):
        return self.__format_gecko_report__(repositories_of_interest=self.getReportRepos())

    def getSkippedRepoReport(self):
        return self.__format_gecko_report__(repositories_of_interest=self.getSkippedRepos())

    def getTeamReport(self):
        data = []
        teams = self.db_client.getTeams().values_list('name', flat=True)

        for team in teams:
            team_report = self.__format_gecko_report__(
                repositories_of_interest=self.getTeamReportRepos(team=team), teams=team)
            data.append({'team': team, 'team_report': team_report})

        return data

    def __format_gecko_report__(self, repositories_of_interest, teams=None):

        gercko_report = list()

        report_repositories = self.db_client.getSortedVunrableRepos(
            repositories=repositories_of_interest)[:20]

        for vulnerable_repository in report_repositories:
            repository = vulnerable_repository.repository.name
            repo_teams = None
            data = {}
            if teams == None:
                repo_teams = list(self.db_client.getRepoTeams(
                    repository=repository).values_list('name', flat=True))

                if len(repo_teams) > 1:
                    repo_teams = f'{repo_teams.pop()}++'
                else:
                    if len(repo_teams) == 1:
                        repo_teams = repo_teams.pop()
                    else:
                        repo_teams = 'None'
            else:
                repo_teams = teams

            data = {
                'repository': repository,
                'critical': vulnerable_repository.critical,
                'high': vulnerable_repository.high,
                'moderate': vulnerable_repository.moderate,
                'low': vulnerable_repository.low
            }

            if teams == None:
                data.update({'teams': repo_teams})

            gercko_report.append(data)

        return gercko_report
