# -*- coding: utf-8 -*-
from report.helper.functions import sort_list_by_total
from config.severities import SEVERITY
from django.conf import settings
from copy import deepcopy
import logging
from common.functions import isinstance_of

logger = logging.getLogger(__name__)


class BuildGeckoReport:
    """
    format report for gecko board

    Variables:
    ----------
    - self.report , hash to hold the report data
    - self._max_report_repositories , defaults to environment variable settings.GECKO_BOARD_TOP_N_REPOSITORIES

    """

    def __init__(self):
        self._report = {"organization": [], "teams": {}}
        self._max_report_repositories = settings.GECKO_BOARD_TOP_N_REPOSITORIES

    def clear(self):
        """
        reset class variables
        """
        self._report = {"organization": [], "teams": {}}
        self._max_report_repositories = settings.GECKO_BOARD_TOP_N_REPOSITORIES

    def __del__(self):
        self.clear()

    @property
    def organization_report(self):
        if self._report["organization"] == []:
            logger.warning(
                "gecko organization report is empty, did you run organization report?"
            )
        return self._report["organization"]

    @property
    def teams_report(self):
        if self._report["teams"] == {}:
            logger.warning("gecko teams report is empty, did you run teams report?")

        return self._report["teams"]

    @property
    def max_report_repositories(self):

        """
        returns the max number of repositories
        """
        return self._max_report_repositories

    @max_report_repositories.setter
    def max_report_repositories(self, max_count):

        """
        Sets max number of repository in report

        Parameters:
        -----------
        max_count: maximum count to set

        Returns:
        --------
        None
        """
        isinstance_of(max_count, int, "max_count")

        self._max_report_repositories = max_count

    def organizaition(self, report_reader):

        """
        GET TOP N repositoies

        Paramters:
        ----------
        report_reader: ReportReader object

        It updates self._report with organization level report

        Returns:
        --------
        None
        """
        repositories_list = sort_list_by_total(
            data=report_reader.organization_repositories_list
        )

        self._processed_data(repositories_list=repositories_list)

    def teams(self, report_reader):

        """
        GET TOP N repositoies

        Paramter:
        ----------
        report_reader: ReportReader object

        It updates self._report with team level report

        Returns:
        --------
        None
        """

        for team in report_reader.teams.keys():
            repositories_list = sort_list_by_total(
                data=report_reader.team_repositories_list(team=team)
            )
            self._processed_data(repositories_list=repositories_list, team=team)

    def _processed_data(self, repositories_list, team=None):

        """
        This displays effective severities count instead of actual

        Paramters:
        -----------
        repositories_list: simply list of sorted repositories
        team_report: this tells if we need to include teams filed in dat or not
                     if it is per team report, we do not need to include team field
                     whilst if it is a organization report we want to include team

        Returns:
        --------
        None
        """

        first_n_repositories = repositories_list[: self.max_report_repositories]

        """
        consider team for dataset if and only if it has least one repository
        """
        if first_n_repositories:

            if team:
                self.teams_report.update({team: []})

            for repository in first_n_repositories:
                severities = repository["total"]["severities"]["original"]
                repository_name = repository["name"]
                critical = severities[SEVERITY.CRITICAL.name]
                high = severities[SEVERITY.HIGH.name]
                moderate = severities[SEVERITY.MODERATE.name]
                low = severities[SEVERITY.LOW.name]

                repository_processed_data = {
                    "repository": repository_name,
                    "critical": critical,
                    "high": high,
                    "moderate": moderate,
                    "low": low,
                }

                if team:
                    self.teams_report[team].append(deepcopy(repository_processed_data))

                else:
                    repository_team = "None"

                    if repository["teams"]:
                        repository_team = repository["teams"].pop(0)

                    repository_processed_data.update({"teams": repository_team})

                    self._report["organization"].append(
                        deepcopy(repository_processed_data)
                    )

            repository_processed_data.clear()
