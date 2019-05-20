import geckoboard as gb
from django.conf import settings
from gecko.helper.fetch import DBReport
from time import sleep
import requests
import json


class GeckoDataSet:

    def __init__(self):
        self.GECKO_API_TOKEN = settings.GECKO_TOKEN
        self.GECKO_OVERVIEW_BOARD = settings.GECKO_OVERVIEW_BOARD
        self.report = DBReport().getReport()
        self.overview_report = DBReport().getOverviewReport()
        try:
            self.gbClient = gb.client(self.GECKO_API_TOKEN)
            self.gbClient.ping()
        except Exception as e:
            raise RuntimeError(e)

        self.count = 0

    def __wait(self):
        # Ensure we are not sending more than 60 updates per minute , this is limit set by Geckoboard
        if self.count >= 50:
            sleep(65)
            self.count = 0

    def __find_or_create_teams_dataset(self):

        for team, alerts in self.report.items():
            self.__wait()
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
            dataset.put(alerts)
            self.count += 3

    # def __find_or_create_overview_dataset(self):

    #     self.__wait()

    #     dataset = self.gbClient.datasets.find_or_create('overview.github.vulnerability.alerts.by_name',
    #                                                     {
    #                                                         'teams': {'type': 'string', 'name': 'Teams'},
    #                                                         'repository': {'type': 'string', 'name': 'Repository'},
    #                                                         'critical': {'type': 'number', 'name': 'C'},
    #                                                         'high': {'type': 'number', 'name': 'H'},
    #                                                         'moderate': {'type': 'number', 'name': 'M'},
    #                                                         'low': {'type': 'number', 'name': 'L'}
    #                                                     },
    #                                                     ['repository']
    #                                                     )
    #     dataset.put([])
    #     dataset.put(self.overview_report)

    def __overviewListBoard(self):
        data = list()

        for info in self.overview_report[:15]:
            data.append(
                {
                    'title':
                    {
                        'text': "C:{} H:{} M:{} L:{}".format(info['critical'], info['high'], info['moderate'], info['low'])
                    },
                    'description': "repository: {} Team(s): {}".format(info['repository'], info['teams'])
                }
            )

        json_data = json.dumps({'api_key': self.GECKO_API_TOKEN, 'data': data})

        request = requests.post(self.GECKO_OVERVIEW_BOARD, data=json_data)

    def push(self):
        self.__find_or_create_teams_dataset()

    def push_overview(self):
        self.__overviewListBoard()
