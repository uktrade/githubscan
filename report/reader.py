# -*- coding: utf-8 -*-
from common.functions import load_json_file, isinstance_of

from django.conf import settings


class ReportReader:
    """
    Class with read only properties to get report data
    """

    def __init__(self):
        """
        Variables:
        -----------
        self._processed_data_store: a dict object to store /load report data
        """
        self._processed_data_store = {}

    def clear(self):
        self._processed_data_store.clear()

    def __del__(self):
        self.clear()

    @property
    def processed_data(self):
        return self._processed_data_store

    @processed_data.setter
    def load_data_from_dict(self, data):
        """loading from dictionay is useful in case of testing"""
        isinstance_of(data, dict, "data")

        self._processed_data_store = dict(data)

    @processed_data.setter
    def load_data_from_file(self, data_file=settings.PROCESSED_DATA_FILE_PATH):
        """Error handling for this is done in load_json_file"""
        data = load_json_file(src_file=data_file)
        self._processed_data_store = dict(data)

    @property
    def enterprise_users(self):
        return self.processed_data["enterprise_users"]

    @property
    def sso_notification_targets(self):
        return self.processed_data["sso_notification_targets"]

    @property
    def users_without_sso_email(self):
        self.processed_data["users_without_sso_email"]

    @property
    def repositories(self):
        return self.processed_data["repositories"]

    @property
    def vulnerable_repositories(self):
        return self.processed_data["vulnerable_repositories"]

    @property
    def token_has_no_access(self):
        return self.processed_data["token_has_no_access"]

    @property
    def teams(self):
        return self.processed_data["teams"]

    @property
    def skip_scan_repositories(self):
        return self.processed_data["skip_scan_repositories"]

    @property
    def orphan_repositories(self):
        return self.processed_data["orphan_repositories"]

    @property
    def organization_severity_status(self):
        return self.processed_data["severity_status"]

    @property
    def organization_total(self):
        return self.processed_data["total"]

    @property
    def organization_repositories_list(self):
        organization_repositories = set(self.repositories.keys()).difference(
            set(self.skip_scan_repositories["list"])
        )

        return [
            repository
            for repositor_name, repository in self.repositories.items()
            if repositor_name in organization_repositories
        ]

    @property
    def reportable_organization_repositories_list(self):

        org_report_repositories_name = set(self.vulnerable_repositories).difference(
            set(self.skip_scan_repositories["list"])
        )

        return [
            repository
            for repositor_name, repository in self.repositories.items()
            if repositor_name in org_report_repositories_name
        ]

    @property
    def sso_notification_targets(self):
        return self.processed_data["sso_notification_targets"]

    @property
    def users_without_sso_email(self):
        return self.processed_data["users_without_sso_email"]

    def team_repositories_list(self, team):

        team_repositories_name = set(self.teams[team]["repositories"]).difference(
            set(self.skip_scan_repositories["list"])
        )

        return [
            repository
            for repositor_name, repository in self.repositories.items()
            if repositor_name in team_repositories_name
        ]

    def reportable_team_repositories_list(self, team):

        team_repositories_name = (
            set(self.teams[team]["repositories"])
            .intersection(self.vulnerable_repositories)
            .difference(set(self.skip_scan_repositories["list"]))
        )

        return [
            repository
            for repositor_name, repository in self.repositories.items()
            if repositor_name in team_repositories_name
        ]
