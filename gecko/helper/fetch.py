from github.helper.fetch.Db import Data
from random import choice


class DBReport:

    def __init__(self):
        self.dbData = Data()

    def getReport(self):
        report = dict()

        team_set = set((self.dbData.getTeams()).values_list('name', flat=True))
        for team in team_set:
            teamrepo_set = set((self.dbData.getTeamRepos(team=team)
                                ).values_list('repository', flat=True))
            alerts = list()
            for repository in teamrepo_set:
                try:
                    alerts_set = self.dbData.getVulnerabilities(
                        repository=repository).values('repository', 'critical', 'high', 'moderate', 'low')[0]

                except IndexError:
                    alerts_set = {'repository': repository, 'critical': -1,
                                  'high': -1, 'moderate': -1, 'low': -1}

                alerts.append(alerts_set)

            report[team] = alerts

        return report

    def getOverviewReport(self):
        vulnerabilities = list()
        repository_set = set(
            (self.dbData.getRepos()).values_list('name', flat=True))

        repository_with_vulnerability_enabled = set(self.dbData.getAllVulnerabilities(
        ).values_list('repository', flat=True))

        repository_with_vulnerability_disabled = repository_set.difference(
            repository_with_vulnerability_enabled)

        # Select top 20 results ordered_by , fields defined in queryset
        vulnerabilities = list(self.dbData.getAllVulnerabilities().order_by(
            '-critical', '-high', 'repository').values('repository', 'critical', 'high', 'moderate', 'low')[:20])

        for repo in repository_with_vulnerability_disabled:
            vulnerabilities.append(
                {'repository': repo, 'critical': -1, 'high': -1, 'moderate': -1, 'low': -1})

        for vulnerability in vulnerabilities:
            repository = vulnerability['repository']
            repoteams_set = set(self.dbData.getRepoteams(
                repository=repository).values_list('team', flat=True))

            if len(repoteams_set) == 0:
                repoteam = 'None'
            else:
                if len(repoteams_set) == 1:
                    repoteam = repoteams_set.pop()
                else:
                    if len(repoteams_set) > 1:
                        repoteam = choice(list(repoteams_set)) + '++'

            vulnerability.update({'teams': repoteam})

        return list(vulnerabilities)
