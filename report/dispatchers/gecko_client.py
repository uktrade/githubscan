# -*- coding: utf-8 -*-
import geckoboard
from common.functions import singleton
from ratelimit import limits, sleep_and_retry
from django.conf import settings


@singleton
class GeckoClient:
    """
    Create Connection and send the report
    We want this to be single tone so we can keep trace of number of request sent
    it needs to be limted to max 60 per minute or 1 per second

    Note: this class is not tested , seems there is not any way to test gecko client
    unless we send actual data, which is probably already tested
    with the geckoboard module
    """

    def __init__(self, api_key=settings.GECKO_BOARD_TOKEN):
        self._gb_cleint = geckoboard.client(api_key)

    @sleep_and_retry
    @limits(calls=1, period=8)
    def send_organization_report(self, organization_data):
        dataset = (
            "overview.github.vulnerability.alerts.by_name",
            {
                "teams": {"type": "string", "name": "Teams"},
                "repository": {"type": "string", "name": "Repository"},
                "critical": {"type": "number", "name": "C"},
                "high": {"type": "number", "name": "H"},
                "moderate": {"type": "number", "name": "M"},
                "low": {"type": "number", "name": "L"},
            },
        )

        self._publish_to_geckoboard_(dataset=dataset, data=organization_data)

    @sleep_and_retry
    @limits(calls=1, period=8)
    def send_team_report(self, team, team_data):
        dataset = (
            team.lower() + ".github.vulnerability.alerts.by_name",
            {
                "repository": {"type": "string", "name": "Repository"},
                "critical": {"type": "number", "name": "C"},
                "high": {"type": "number", "name": "H"},
                "moderate": {"type": "number", "name": "M"},
                "low": {"type": "number", "name": "L"},
            },
        )

        self._publish_to_geckoboard_(dataset=dataset, data=team_data)

    def _publish_to_geckoboard_(self, dataset, data):
        """
        This method publishes dataset to gecko board
        """
        try:
            self._gb_cleint.ping()
            gb_dataset = self._gb_cleint.datasets.find_or_create(dataset[0], dataset[1])

            """
            clean it before updating
            """
            gb_dataset.put([])
            gb_dataset.put(data)

        except:
            raise
