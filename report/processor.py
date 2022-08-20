# -*- coding: utf-8 -*-
from common.functions import load_json_file, isinstance_of
from report.helper.day_manager import DayManager
from report.helper.uk_holidays import UKHolidays
from django.conf import settings

from config.severities import (
    EFFECTIVE_SEVERITY,
    SEVERITY,
    ESCALATION_RULES,
    SEVERITY_STATUS,
    TIME_TO_FIX,
)

from collections import Counter
from copy import deepcopy


class ReportDataProcessor:
    """Class to parse scanner data and make it useful for reporting"""

    def __init__(self):
        """
        Variables
        ----------
        self._processed_data_store : dict , holds processed data and, we intially initalize it with scanned data
        self._scanned_data_store: dict , scanned data which can be loaded from file or a dict
        self._uk_holidays: UKHolidays , used by DayManager
        self.day_manager: DayManager, to perform date related calculations
        """
        self._processed_data_store = {}
        self._scanned_data_store = {}
        self._uk_holidays = UKHolidays(
            data_file=settings.UK_HOLIDAYS_FILE_PATH,
            max_data_file_age=settings.UK_HOLIDAYS_FILE_MAX_AGE,
        )
        self._uk_holidays.calendar_url = settings.UK_HOLIDAYS_SOURCE_URL
        self.day_manager = DayManager(uk_holidays=self._uk_holidays.calendar)

        """Dict to keep the total counts across multiple fields """
        self._total = dict(
            {
                "repositories": 0,
                "severities": {
                    "effective": {
                        EFFECTIVE_SEVERITY.CRITICAL_BREACH.name: 0,
                        EFFECTIVE_SEVERITY.CRITICAL.name: 0,
                        EFFECTIVE_SEVERITY.HIGH.name: 0,
                        EFFECTIVE_SEVERITY.MODERATE.name: 0,
                        EFFECTIVE_SEVERITY.LOW.name: 0,
                    },
                    "original": {
                        SEVERITY.CRITICAL.name: 0,
                        SEVERITY.HIGH.name: 0,
                        SEVERITY.MODERATE.name: 0,
                        SEVERITY.LOW.name: 0,
                    },
                },
                "slo_breach": {
                    "repositories": 0,
                    "severities": {
                        SEVERITY.CRITICAL.name: 0,
                        SEVERITY.HIGH.name: 0,
                        SEVERITY.MODERATE.name: 0,
                        SEVERITY.LOW.name: 0,
                    },
                },
            }
        )

        self._processed_data_store = {
            "enterprise_users": {},
            "sso_notification_targets": {},
            "repositories": {},
            "teams": {},
            "vulnerable_repositories": [],
            "skip_scan_repositories": {},
            "orphan_repositories": {},
            "users_without_sso_email": [],
            "token_has_no_access": [],
            "severity_status": "",
            "total": deepcopy(self._total),
        }

    def clear(self):
        self._scanned_data_store.clear()
        self._processed_data_store = {
            "enterprise_users": {},
            "sso_notification_targets": {},
            "repositories": {},
            "teams": {},
            "vulnerable_repositories": [],
            "skip_scan_repositories": {},
            "orphan_repositories": {},
            "users_without_sso_email": [],
            "token_has_no_access": [],
            "severity_status": "",
            "total": deepcopy(self._total),
        }

    def __del__(self):
        self.clear()

    @property
    def processed_data(self):
        return self._processed_data_store

    @property
    def enterprise_users(self):
        "return enterprise users dict"
        return self.processed_data["enterprise_users"]

    @property
    def repositories(self):
        "returns repositories dict"
        return self.processed_data["repositories"]

    @property
    def teams(self):
        "returns teams dict"
        return self.processed_data["teams"]

    @property
    def vulnerable_repositories(self):
        """returns read only list of vulnerable repositories"""
        return self.processed_data["vulnerable_repositories"]

    @property
    def skip_scan_repositories(self):
        "returns skip scan repositories dict"
        return self.processed_data["skip_scan_repositories"]

    @property
    def orphan_repositories(self):
        "returns orphan repositories dict"
        return self.processed_data["orphan_repositories"]

    @orphan_repositories.setter
    def orphan_repositories(self, repository_list):

        isinstance_of(repository_list, list, "repository_list")

        self.processed_data["orphan_repositories"].update({"list": repository_list})

    @property
    def token_has_no_access(self):
        "returns list of unique token_has_no_access repositories"
        return list(set(self.processed_data["token_has_no_access"]))

    @token_has_no_access.setter
    def token_has_no_access(self, repository_list):

        isinstance_of(repository_list, list, "repository_list")

        self.processed_data["token_has_no_access"] = repository_list

    @property
    def scanned_data(self):
        return self._scanned_data_store

    @property
    def sso_notification_targets(self):
        return self._processed_data_store["sso_notification_targets"]

    @property
    def users_without_sso_email(self):
        return self._processed_data_store["users_without_sso_email"]

    @scanned_data.setter
    def load_data_from_dict(self, data):
        """loading from dictionay is useful in case of testing"""
        isinstance_of(data, dict, "data")

        self._scanned_data_store = dict(data)

    @scanned_data.setter
    def load_data_from_file(self, data_file):
        """Error handling for this is done in load_json_file"""
        data = load_json_file(src_file=data_file)
        self._scanned_data_store = dict(data)

    def add_enterprise_users(self):
        """
        This method simply copies all enterprise users from scanned data to processed data as it is
        """
        self._processed_data_store["enterprise_users"] = self._scanned_data_store[
            "enterprise_users"
        ]

    def add_sso_notification_targets(self):
        known_users = self._scanned_data_store["enterprise_users"]
        team_members = self._scanned_data_store["team_members"]

        for team, members in team_members.items():
            if team not in self._processed_data_store["sso_notification_targets"]:
                self._processed_data_store["sso_notification_targets"].update(
                    {team: {}}
                )

            for member in members:
                if member in known_users:
                    self._processed_data_store["sso_notification_targets"][team].update(
                        {member: known_users[member]["email"]}
                    )
                    continue

                self._processed_data_store["users_without_sso_email"].append(member)

    def add_repositories(self):
        """
        This method takes a list of repositories from scanner data and
        creates the repositories dict for reporting purpose
        """
        for repository in self._scanned_data_store["repositories"]:
            self._processed_data_store["repositories"].update(
                {repository["name"]: repository}
            )

    def add_repository_teams(self):
        """
        This methods adds teams to repository

        Dependencies
        -------------
        - add_repositories
        """
        for team_info in self.scanned_data["team_repositories"]:
            for team, team_repositories in team_info.items():
                for repository_name in team_repositories:
                    if repository_name in self._processed_data_store["repositories"]:
                        self._processed_data_store["repositories"][repository_name][
                            "teams"
                        ].append(team)

    def add_teams_and_team_repositories(self):
        """simply addeds teams and repositories data to report data"""
        for team in self.scanned_data["teams"]:
            self.teams.update({team: {"repositories": []}})
            self.teams.update({team: {"name": team}})

        for team_info in self.scanned_data["team_repositories"]:
            for team, team_repositories in team_info.items():
                self.teams[team]["repositories"] = list(team_repositories)

    def enforce_exclusive_team_repositories(self, exclusive_team="default"):
        """
        repositories for exclusive_team should be exclusively for that team only
        so we will remove it here from other teams

        Case that we have here is for example repository X is to host some kind of
        documentation ( Sphnix to host rst based docs for e.g. ) , everyone in organization
        needs to be able to push ( i.e. write to it) , however only Documentation team is
        responsible for managing vulnerability and repository.

        So we will need to enforce this relation, if not , everyone with write access ( i.e. all/every team in this case)
        will receive the alerts and, certainly they would not like it!

        Dependencies
        --------------
        - add_repositories
        - add_teams_and_team_repositories

        Note, this method is not tested at the moment because
        test generator dose not support this kind of scenairo just yet
        """
        if exclusive_team in self.teams.keys():
            exclusive_repositories = set(self.teams[exclusive_team]["repositories"])

            """
            Code below removes repositories from the other teams
            """
            for team, team_info in self.teams.items():
                team_repo_set = set(team_info["repositories"])
                team_relavent_set = team_repo_set.difference(exclusive_repositories)
                if team_relavent_set:
                    self.teams[team]["repositories"] = list(team_relavent_set)

            """
            Code below removes other teams from exclusive_repositories
            """
            for repository_name in exclusive_repositories:
                self.repositories[repository_name]["teams"] = [exclusive_team]

    def add_vulnerable_repositories(self):
        """
        Builds list of vulnurable repositories

        Dependencies
        --------------
        - add_repositories
        """
        vulnerable_repositories = [
            repository["name"]
            for repository in self.processed_data["repositories"].values()
            if repository["alerts"]
        ]

        self.processed_data.update({"vulnerable_repositories": vulnerable_repositories})

    def add_token_has_no_access(self):
        """
        This method
        - updates self._processed_data_store to add token_has_noaccess
        - returns nothing
        token_has_no_access is a situation which was observed during working on this project where
        - repository is not archived ( they are already filtered in query )
        - repository is not present in repositories key ( i.e. not fetched by repositories query )
        - repository is listed under team i.e. some team has ADMIN,MAINTAIN or WRITE permission

        Dependencies:
        --------------
        - add_repositories
        - add_teams_and_team_repositories
        """

        scanned_repositories = set(self.repositories.keys())

        for team_info in self.teams.values():
            team_repositories = set(team_info["repositories"])

            if team_repositories.issubset(scanned_repositories):
                continue

            self.token_has_no_access += list(
                team_repositories.difference(scanned_repositories)
            )

    def add_severity_age_in_days(self):
        """
        This method adds:
            - severity age in business days
            - severity age in calendar days

        Dependencies:
        --------------
        - add_repositories
        - add_vulnerable_repositories
        """

        for repository_name in self.vulnerable_repositories:
            for alert in self.repositories[repository_name]["alerts"]:
                created_at = self.day_manager.str_datetime_to_date(alert["createdAt"])
                age_in_business_days = self.day_manager.business_days_between(
                    start_date=created_at
                )
                age_in_calendar_days = self.day_manager.calendar_days_between(
                    start_date=created_at
                )

                alert.update(
                    {
                        "age_in_business_days": age_in_business_days,
                        "age_in_calendar_days": age_in_calendar_days,
                    }
                )

    def add_effective_level_and_escalation_status(self):
        """
        This method adds:
            - effective_level
            - escalated

        Dependencies:
        --------------
        - add_repositories
        - add_vulnerable_repositories
        - add_severity_age_in_days
        """
        for repository_name in self.vulnerable_repositories:
            for alert in self.repositories[repository_name]["alerts"]:
                original_level = alert["level"]
                effective_level = alert["level"]
                escalated = False

                if alert["age_in_business_days"] > TIME_TO_FIX[original_level]:
                    escalated = True

                    for escalated_severity in range(
                        EFFECTIVE_SEVERITY.CRITICAL_BREACH.value,
                        SEVERITY[original_level].value,
                        -1,
                    ):
                        escalated_severity_level = EFFECTIVE_SEVERITY(
                            escalated_severity
                        ).name
                        time_to_fix_escalation = ESCALATION_RULES[original_level][
                            escalated_severity_level
                        ]

                        if alert["age_in_business_days"] > time_to_fix_escalation:
                            effective_level = escalated_severity_level
                            break

                alert.update(
                    {"escalated": escalated, "effective_level": effective_level}
                )

    def add_fix_by_date(self):
        """
        This method adds:
            - fix_by : date one must fix the vulnerability by to avoid critical breach

        Dependencies:
        --------------
        - add_repositories
        - add_vulnerable_repositories
        """
        for repository_name in self.vulnerable_repositories:
            for alert in self.repositories[repository_name]["alerts"]:
                original_level = alert["level"]
                created_at = self.day_manager.str_datetime_to_date(alert["createdAt"])
                business_days_to_avoid_CRITICAL_BREACH = ESCALATION_RULES[
                    original_level
                ][EFFECTIVE_SEVERITY.CRITICAL_BREACH.name]

                calendar_days_to_avoid_CRITICAL_BREACH = (
                    self.day_manager.business_days_to_calendar_days(
                        start_date=created_at,
                        business_days=business_days_to_avoid_CRITICAL_BREACH,
                    )
                )

                fix_by = self.day_manager.end_date(
                    start_date=created_at,
                    calendar_days=calendar_days_to_avoid_CRITICAL_BREACH,
                )

                """ Todo day manager work out working days to fix"""
                alert.update(
                    {
                        "days_to_fix": self.day_manager.working_days_between_dates(
                            end_date=fix_by
                        )
                    }
                )
                alert.update({"fix_by": self.day_manager.date_to_str_date(fix_by)})

    def add_hash(self):
        """
        This method adds hash of altert data to alert, which would later allow us to determine uniq set of alerts

        Dependencies:
        --------------
        - add_repositories
        - add_vulnerable_repositories
        - add_effective_level_and_escalation_status
        - add_fix_by_date
        """
        for repository_name in self.vulnerable_repositories:
            for alert in self.repositories[repository_name]["alerts"]:
                level = alert["level"]
                effective_level = alert["effective_level"]
                package_name = alert["package"]
                patched_version = alert["patched_version"]
                fix_by = alert["fix_by"]

                hash_value = hash(
                    f"{level}{effective_level}{package_name}{patched_version}{fix_by}"
                )

                alert.update({"hash": hash_value})

    def add_repository_severity_status(self):
        """
        This method adds severity_status
        GREEN: if no vulnerability is found or no vulnerability has been escalated
        AMBER: if vulnerability is escalated but not a CRITICAL_BREACH
        RED: if CRITICAL_BREACH

        Dependencies
        ------------
        - add_repositories
        - add_vulnerable_repositories
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        """

        clean_repositories = set(self.repositories.keys()).difference(
            set(self.vulnerable_repositories)
        )

        for repository_name in clean_repositories:
            self.repositories[repository_name].update(
                {"severity_status": SEVERITY_STATUS.CLEAN.name}
            )

        for repository_name in self.vulnerable_repositories:
            repository = self.repositories[repository_name]

            effective_levels = [
                alert["effective_level"] for alert in repository["alerts"]
            ]

            if EFFECTIVE_SEVERITY.CRITICAL_BREACH.name in effective_levels:
                repository.update({"severity_status": SEVERITY_STATUS.RED.name})
                continue

            escalated_status = [alert["escalated"] for alert in repository["alerts"]]

            if True in escalated_status:
                repository.update({"severity_status": SEVERITY_STATUS.AMBER.name})
                continue

            repository.update({"severity_status": SEVERITY_STATUS.GREEN.name})

    def add_repository_totals(self):
        """
        Add total count for each severity level with in given repository

        Dependencies
        -------------
        - add_repositories
        - add_vulnerable_repositories
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        """

        for repository in self.repositories.values():

            total = deepcopy(self._total)

            if repository["name"] in self.vulnerable_repositories:

                orignal_severity_counter = Counter()
                effective_severity_counter = Counter()
                slo_breach_counter = Counter()

                for alert in repository["alerts"]:
                    orignal_severity_counter[alert["level"]] += 1
                    effective_severity_counter[alert["effective_level"]] += 1

                    if alert["escalated"]:
                        slo_breach_counter[alert["level"]] += 1

                for severity, count in orignal_severity_counter.items():
                    total["severities"]["original"][severity] = count

                for severity, count in effective_severity_counter.items():
                    total["severities"]["effective"][severity] = count

                for severity, count in slo_breach_counter.items():
                    total["slo_breach"]["severities"][severity] = count
                    total["slo_breach"]["repositories"] = 1

                total["repositories"] = 1

            repository.update({"total": total})

    def add_skip_scan_repositories(self):
        """
        based on the topics set it adds and sets the boolean key hasSkipScan to each repository
        Dependencies
        -------------
        - add_repositories
        """

        self.skip_scan_repositories.update({"list": []})
        for repository in self.repositories.values():
            repository.update({"hasSkipScan": False})
            if settings.GITHUB_SKIP_SCAN_TOPIC in repository["topics"]:
                repository["hasSkipScan"] = True
                self.skip_scan_repositories["list"].append(repository["name"])

    def add_skip_scan_repositories_severity_status(self):
        """
        Dependencies
        --------------
        - add_repositories
        - add_vulnerable_repositories
        - add_teams_and_team_repositories
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        - add_repository_severity_status
        - add_skip_scan_repositories_severity_status
        """
        self.skip_scan_repositories.update(
            {"severity_status": SEVERITY_STATUS.CLEAN.name}
        )

        repositories_with_info = set(self.skip_scan_repositories["list"]).intersection(
            self.vulnerable_repositories
        )

        if repositories_with_info:

            severity_status_counter = Counter()

            for repository_name in repositories_with_info:
                severity_status_counter[
                    self.repositories[repository_name]["severity_status"]
                ] += 1

            if severity_status_counter[SEVERITY_STATUS.RED.name] > 0:
                self.skip_scan_repositories[
                    "severity_status"
                ] = SEVERITY_STATUS.RED.name

            elif severity_status_counter[SEVERITY_STATUS.AMBER.name] > 0:
                self.skip_scan_repositories[
                    "severity_status"
                ] = SEVERITY_STATUS.AMBER.name

            elif severity_status_counter[SEVERITY_STATUS.GREEN.name] > 0:
                self.skip_scan_repositories[
                    "severity_status"
                ] = SEVERITY_STATUS.GREEN.name

    def add_skip_scan_repositories_totals(self):
        """
        Dependencies
        --------------
        - add_repositories
        - add_vulnerable_repositories
        - add_teams_and_team_repositories
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        - add_repository_severity_status
        - add_skip_scan_repositories
        """
        self.skip_scan_repositories.update({"total": deepcopy(self._total)})

        repositories_with_info = set(self.skip_scan_repositories["list"]).intersection(
            self.vulnerable_repositories
        )

        if repositories_with_info:
            original_severity_count = Counter()
            effective_severity_count = Counter()
            slo_breach_counter = Counter()
            slo_breach_repositories_counter = 0

            for repository_name in repositories_with_info:

                for severity, count in self.repositories[repository_name]["total"][
                    "severities"
                ]["original"].items():
                    original_severity_count[severity] += count

                for severity, count in self.repositories[repository_name]["total"][
                    "severities"
                ]["effective"].items():
                    effective_severity_count[severity] += count

                for severity, count in self.repositories[repository_name]["total"][
                    "slo_breach"
                ]["severities"].items():
                    slo_breach_counter[severity] += count

                slo_breach_repositories_counter += self.repositories[repository_name][
                    "total"
                ]["slo_breach"]["repositories"]

            for severity, count in original_severity_count.items():
                self.skip_scan_repositories["total"]["severities"]["original"][
                    severity
                ] = count

            for severity, count in effective_severity_count.items():
                self.skip_scan_repositories["total"]["severities"]["effective"][
                    severity
                ] = count

            for severity, count in slo_breach_counter.items():
                self.skip_scan_repositories["total"]["slo_breach"]["severities"][
                    severity
                ] = count

            self.skip_scan_repositories["total"]["slo_breach"][
                "repositories"
            ] = slo_breach_repositories_counter
            self.skip_scan_repositories["total"]["repositories"] = len(
                repositories_with_info
            )

    def add_team_severity_status(self):
        """
        Adds severity status to team based on collection of repositories status for team
        i.e.
        RED: if even one repository severity_status assigned red
        AMBER: if no repository severity_status is RED however there is least one AMBER
        GREEN: if all severity_status are green
        CLEAN: if all severity_status are Clean ( not implemented )
          Dependencies
        -------------
        - add_repositories
        - add_vulnerable_repositories
        - add_teams_and_team_repositories
        - add_token_has_no_access
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        - add_repository_severity_status
        - add_skip_scan_repositories
        """

        for team, team_info in self.teams.items():
            self.teams[team].update({"severity_status": SEVERITY_STATUS.CLEAN.name})

            team_repositories = set(team_info["repositories"])

            repositories_with_info = team_repositories.difference(
                set(self.token_has_no_access),
                set(self.skip_scan_repositories["list"]),
            ).intersection(set(self.vulnerable_repositories))

            if repositories_with_info:

                severity_status_counter = Counter()

                for repository_name in repositories_with_info:
                    severity_status_counter[
                        self.repositories[repository_name]["severity_status"]
                    ] += 1

                if severity_status_counter[SEVERITY_STATUS.RED.name] > 0:
                    self.teams[team]["severity_status"] = SEVERITY_STATUS.RED.name

                elif severity_status_counter[SEVERITY_STATUS.AMBER.name] > 0:
                    self.teams[team]["severity_status"] = SEVERITY_STATUS.AMBER.name

                elif severity_status_counter[SEVERITY_STATUS.GREEN.name] > 0:
                    self.teams[team]["severity_status"] = SEVERITY_STATUS.GREEN.name

    def add_team_totals(self):
        """
        Here, we need to be slightly careful about not to account for
            - repositories with skip scan topic set
            - repositories which are part of token_has_no_access

        Dependencies
        -------------
        - add_repositories
        - add_vulnerable_repositories
        - add_teams_and_team_repositories
        - add_token_has_no_access
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        - add_repository_totals
        - add_skip_scan_repositories
        """
        for team, team_info in self.teams.items():
            self.teams[team].update({"total": deepcopy(self._total)})

            team_repositories = set(team_info["repositories"])

            repositories_with_info = team_repositories.difference(
                set(self.token_has_no_access), set(self.skip_scan_repositories["list"])
            ).intersection(self.vulnerable_repositories)

            if repositories_with_info:
                original_severity_counter = Counter()
                effective_severity_counter = Counter()
                slo_breach_counter = Counter()
                slo_breach_repositories_counter = 0

                for repository_name in repositories_with_info:
                    for severity, count in self.repositories[repository_name]["total"][
                        "severities"
                    ]["original"].items():
                        original_severity_counter[severity] += count

                    for severity, count in self.repositories[repository_name]["total"][
                        "severities"
                    ]["effective"].items():
                        effective_severity_counter[severity] += count

                    for severity, count in self.repositories[repository_name]["total"][
                        "slo_breach"
                    ]["severities"].items():
                        slo_breach_counter[severity] += count

                    slo_breach_repositories_counter += self.repositories[
                        repository_name
                    ]["total"]["slo_breach"]["repositories"]

                self.teams[team]["total"]["severities"][
                    "original"
                ] = original_severity_counter
                self.teams[team]["total"]["severities"][
                    "effective"
                ] = effective_severity_counter

                self.teams[team]["total"]["slo_breach"][
                    "repositories"
                ] = slo_breach_repositories_counter
                self.teams[team]["total"]["slo_breach"][
                    "severities"
                ] = slo_breach_counter

            self.teams[team]["total"]["repositories"] = len(repositories_with_info)

    def add_organization_severity_status(self):
        """
        In this method we will account for
        - orphan repository
        However, we will not account for
        - hasSkipScan True ( i.e. skipped repository)

        Dependencies
        ------------
        - add_repositories
        - add_vulnerable_repositories
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        - add_skip_scan_repositories
        - add_repository_severity_status
        """

        self.processed_data.update({"severity_status": SEVERITY_STATUS.CLEAN.name})

        repositories_with_info = (
            set(self.repositories.keys()).difference(
                set(self.skip_scan_repositories["list"])
            )
        ).intersection(set(self.vulnerable_repositories))

        if repositories_with_info:
            severity_status_list = [
                self.repositories[repository_name]["severity_status"]
                for repository_name in repositories_with_info
            ]
            if SEVERITY_STATUS.RED.name in severity_status_list:
                self._processed_data_store["severity_status"] = SEVERITY_STATUS.RED.name

            elif SEVERITY_STATUS.AMBER.name in severity_status_list:
                self._processed_data_store[
                    "severity_status"
                ] = SEVERITY_STATUS.AMBER.name

            elif SEVERITY_STATUS.GREEN.name in severity_status_list:
                self._processed_data_store[
                    "severity_status"
                ] = SEVERITY_STATUS.GREEN.name

    def add_organization_totals(self):
        """
        In this method we will account for
        - orphan repository
        However, we will not account for
        - hasSkipScan True ( i.e. skipped repository)
          Dependencies
        ------------
        - add_repositories
        - add_vulnerable_repositories
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        - add_skip_scan_repositories
        - add_repository_totals
        """
        repositories_with_info = (
            set(self.repositories.keys())
            .difference(set(self.skip_scan_repositories["list"]))
            .intersection(self.vulnerable_repositories)
        )

        self.processed_data["total"] == deepcopy(self._total)

        if repositories_with_info:
            original_severity_counter = Counter()
            effective_severity_counter = Counter()
            slo_breach_counter = Counter()
            slo_breach_repositories_counter = 0

            for repository_name in repositories_with_info:
                for severity, count in self.repositories[repository_name]["total"][
                    "severities"
                ]["original"].items():
                    original_severity_counter[severity] += count

                for severity, count in self.repositories[repository_name]["total"][
                    "severities"
                ]["effective"].items():
                    effective_severity_counter[severity] += count

                for severity, count in self.repositories[repository_name]["total"][
                    "slo_breach"
                ]["severities"].items():
                    slo_breach_counter[severity] += count

                slo_breach_repositories_counter += self.repositories[repository_name][
                    "total"
                ]["slo_breach"]["repositories"]

            self.processed_data["total"]["severities"][
                "original"
            ] = original_severity_counter

            self.processed_data["total"]["severities"][
                "effective"
            ] = effective_severity_counter

            self.processed_data["total"]["slo_breach"][
                "severities"
            ] = slo_breach_counter

            self.processed_data["total"]["slo_breach"][
                "repositories"
            ] = slo_breach_repositories_counter

            self.processed_data["total"]["repositories"] = len(repositories_with_info)

    def add_orphan_repositories(self):
        """
        Pick out orhpan repositories i.e.
         - repository found by org token
         - repository not ownwed by team , that is no team has ADMIN,MAINTAINER or WRITE permission on repository

        Dependencies
        --------------
         - add_repositories
         - add_teams_and_team_repositories
        """
        team_repositories = []
        for team_info in self.teams.values():
            team_repositories += team_info["repositories"]

        team_repositories = set(team_repositories)
        organization_repositories = set(self.repositories.keys())

        self.orphan_repositories = list(
            organization_repositories.difference(team_repositories)
        )

    def add_orphan_repositories_severity_status(self):
        """

        Dependencies
        --------------
        - add_repositories
        - add_vulnerable_repositories
        - add_teams_and_team_repositories
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        - add_repository_severity_status
        - add_orphan_repositories
        """

        repositories_with_info = set(self.orphan_repositories["list"]).intersection(
            set(self.vulnerable_repositories)
        )

        self.orphan_repositories.update({"severity_status": SEVERITY_STATUS.CLEAN.name})

        if repositories_with_info:
            severity_status_list = [
                self.repositories[repository_name]["severity_status"]
                for repository_name in repositories_with_info
            ]

            if SEVERITY_STATUS.RED.name in severity_status_list:
                self.orphan_repositories["severity_status"] = SEVERITY_STATUS.RED.name

            elif SEVERITY_STATUS.AMBER.name in severity_status_list:
                self.orphan_repositories["severity_status"] = SEVERITY_STATUS.AMBER.name

            elif SEVERITY_STATUS.GREEN.name in severity_status_list:
                self.orphan_repositories["severity_status"] = SEVERITY_STATUS.GREEN.name

    def add_orphan_repositories_totals(self):
        """
        Dependencies
        --------------
        - add_repositories
        - add_vulnerable_repositories
        - add_teams_and_team_repositories
        - add_severity_age_in_days
        - add_effective_level_and_escalation_status
        - add_repository_severity_status
        - add_orphan_repositories
        """
        self.orphan_repositories.update({"total": deepcopy(self._total)})

        repositories_with_info = set(self.orphan_repositories["list"]).intersection(
            set(self.vulnerable_repositories)
        )

        if repositories_with_info:
            original_severity_counter = Counter()
            effective_severity_counter = Counter()
            slo_breach_counter = Counter()
            slo_breach_repositories_counter = 0

            for repository_name in repositories_with_info:

                for severity, count in self.repositories[repository_name]["total"][
                    "severities"
                ]["original"].items():
                    original_severity_counter[severity] += count

                for severity, count in self.repositories[repository_name]["total"][
                    "severities"
                ]["effective"].items():
                    effective_severity_counter[severity] += count

                for severity, count in self.repositories[repository_name]["total"][
                    "slo_breach"
                ]["severities"].items():
                    slo_breach_counter[severity] += count

                slo_breach_repositories_counter += self.repositories[repository_name][
                    "total"
                ]["slo_breach"]["repositories"]

            self.orphan_repositories["total"]["severities"][
                "original"
            ] = original_severity_counter
            self.orphan_repositories["total"]["severities"][
                "effective"
            ] = effective_severity_counter

            self.orphan_repositories["total"]["slo_breach"][
                "severities"
            ] = slo_breach_counter
            self.orphan_repositories["total"]["slo_breach"][
                "repositories"
            ] = slo_breach_repositories_counter

        self.orphan_repositories["total"]["repositories"] = len(repositories_with_info)
