import geckoboard as gb
from django.conf import settings
from gecko.helper.fetch import DBReport


class GeckoDataSet:

    def __init__(self):
        self.GECKO_API_TOKEN = settings.GECKO_TOKEN
        self.report = DBReport().getReport()
        self.overview_report = DBReport().getOverviewReport()
        try:
            self.gbClient = gb.client(self.GECKO_API_TOKEN)
            self.gbClient.ping()
        except Exception as e:
            raise RuntimeError(e)

    def __find_or_create_teams_dataset(self):

        for team, alters in self.report.items():

            dataset = self.gbClient.datasets.find_or_create(
                team + 'github.vulnerability.alerts.by_name',
                {
                    'repository': {'type': 'string', 'name': 'Repository'},
                    'critical': {'type': 'number', 'name': 'C'},
                    'high': {'type': 'number', 'name': 'H'},
                    'moderate': {'type': 'number', 'name': 'M'},
                    'low': {'type': 'number', 'name': 'L'}
                },
                ['repository']
            )

            dataset.put([])

            formated_data = []

            for alert in alters:
                formated_data.append(alert)

            dataset.put(formated_data)

    def __overview(self):

        for repository, alters in self.overview_report.items():

            dataset = self.gbClient.datasets.find_or_create('overview.github.vulnerability.alerts.by_name',
                                                            {
                                                                'teams': {'type': 'string', 'name': 'Teams'},
                                                                'repository': {'type': 'string', 'name': 'Repository'},
                                                                'critical': {'type': 'number', 'name': 'C'},
                                                                'high': {'type': 'number', 'name': 'H'},
                                                                'moderate': {'type': 'number', 'name': 'M'},
                                                                'low': {'type': 'number', 'name': 'L'}
                                                            },
                                                            ['repository']
                                                            )

            dataset.put([])

            formated_data = []

            for alert in alters:
                formated_data.append(alert)

            dataset.put(formated_data)

    def push(self):
        self.__find_or_create_teams_dataset()

    def push_overview(self):
        self.__overview()
