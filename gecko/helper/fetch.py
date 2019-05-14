from github.helper.fetch.Db import Data


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
        report = dict()
        repository_set = set(
            (self.dbData.getRepos()).values_list('name', flat=True))

        for repository in repository_set:
            repoteams_set = set(self.dbData.getRepoteams(
                repository=repository).values_list('team', flat=True))
            repoteams = ' '.join(list(repoteams_set))

            try:
                alerts_set = self.dbData.getVulnerabilities(
                    repository=repository).values('repository', 'critical', 'high', 'moderate', 'low')[0]

            except IndexError:
                alerts_set = {'repository': repository, 'critical': -
                              1, 'high': -1, 'moderate': -1, 'low': -1}

            alerts_set.update({'teams': repoteams[:100]})

            report[repository] = alerts_set

        return report
