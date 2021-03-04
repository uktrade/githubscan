
from github.report.gecko import GeskoReport
import geckoboard as gb

from django.conf import settings

from django.core.management.base import BaseCommand
from django.conf import settings

from time import sleep
import traceback


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.send_gecko_report()

    def send_gecko_report(self):
        self.count = 0
        GECKO_API_TOKEN = settings.GECKO_TOKEN
        report = GeskoReport()
        try:
            gbClient = gb.client(GECKO_API_TOKEN)
            gbClient.ping()
            self.__push_overview__(gbClient=gbClient, report=report)
            self.__push_teams_report__(gbClient=gbClient, report=report)
        except Exception as e:
            print("GeckoReport Error:{}".format(e))
            traceback.print_exc()

    ### overview report ###
    def __push_overview__(self, gbClient, report):
        self.__wait__()

        dataset = gbClient.datasets.find_or_create('overview.github.vulnerability.alerts.by_name',
                                                   {
                                                       'teams': {'type': 'string', 'name': 'Teams'},
                                                       'repository': {'type': 'string', 'name': 'Repository'},
                                                       'critical': {'type': 'number', 'name': 'C'},
                                                       'high': {'type': 'number', 'name': 'H'},
                                                       'moderate': {'type': 'number', 'name': 'M'},
                                                       'low': {'type': 'number', 'name': 'L'}
                                                   },
                                                   )
        dataset.put([])
        dataset.put(report.getReport())

        self.count += 3

    ### Teams Report ####
    def __push_teams_report__(self, gbClient, report):

        for report in report.getTeamReport():
            self.__wait__()
            team = report['team']
            report_data = report['team_report']

            dataset = gbClient.datasets.find_or_create(
                team + '.github.vulnerability.alerts.by_name',
                {
                    'repository': {'type': 'string', 'name': 'Repository'},
                    'critical': {'type': 'number', 'name': 'C'},
                    'high': {'type': 'number', 'name': 'H'},
                    'moderate': {'type': 'number', 'name': 'M'},
                    'low': {'type': 'number', 'name': 'L'}
                },
            )

            dataset.put([])
            dataset.put(report_data)
            self.count += 3

    # wait if count if more than 50
    # This is to ensure we are not sending more than 60 push request a minute as per the limit set by Geckoboard
    def __wait__(self):
        if self.count >= 50:
            sleep(65)
            self.count = 0
