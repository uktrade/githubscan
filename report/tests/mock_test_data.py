# -*- coding: utf-8 -*-
from report.helper.uk_holidays import UKHolidays
from report.helper.day_manager import DayManager
from django.conf import settings

from config.severities import (
    ESCALATION_RULES,
    SEVERITY,
    EFFECTIVE_SEVERITY,
    SEVERITY_STATUS,
    TIME_TO_FIX,
)
import string
import random

from config.schema import scanner_data_schema
from common.functions import write_json_file


class MockTestData:
    """
    This Class generates mock test data, which has same schema as the real data
    and tests for following scenarios

    Note: Clean status is not implemented in reporting so far

    Repository Status(Both Owned and Orphans):
    -----------------------------------------
    RED  : Meaning, there is least one CRITICAL BREACH
    AMBER: Meaning, There is no CRITICAL BREACH , however one or more Severity has been escalated_severity to higher level
    GREEN: Meaning, There is no breach in any alerts
    CLEAN: Meaning, there is No alert

    Status Propgation To Teams:
    ---------------------------
    RED  : if one more more repository is in RED status with in Team OWNED repositories
    AMBER: if no repository is RED and one ore more repository is AMBER with in Team OWNED repositories
    GREEN: if no repository is RED or AMBER with in Team OWNED repositories
    CLEAN: if no repository with in Team contains a single alert

    Status Propagation to  Organization ( this excludes repository token can not access )
    ------------------------------------
    RED  : if one or more repositories with in Organization is RED
    AMBER: if one or more repositories with in Organization is AMBER
    GREEN: if no repository with in Organization is RED or AMBER
    CLEAN: if no repository with on Organization contains a single alert

    """

    def __init__(self):
        self._alert_combinations = {
            SEVERITY_STATUS.RED.name: {},
            SEVERITY_STATUS.AMBER.name: {},
            SEVERITY_STATUS.GREEN.name: [],
            SEVERITY_STATUS.CLEAN.name: [],
        }
        """
        alert sets going to be of following structure for each status eg.
        red alert set
        red:[
                [ { alert 1}, {alert2} ...],
                [ { alert 1}],
                ...
            ]
        """
        self._alert_combinations = {
            SEVERITY_STATUS.RED.name: {},
            SEVERITY_STATUS.AMBER.name: {},
            SEVERITY_STATUS.GREEN.name: {},
            SEVERITY_STATUS.CLEAN.name: {},
        }
        self._alert_sets = {
            SEVERITY_STATUS.RED.name: [],
            SEVERITY_STATUS.AMBER.name: [],
            SEVERITY_STATUS.GREEN.name: [],
            SEVERITY_STATUS.CLEAN.name: [],
        }

        self._mock_scenarios = {}

        self._uk_holidays = UKHolidays(
            data_file=settings.UK_HOLIDAYS_FILE_PATH,
            max_data_file_age=settings.UK_HOLIDAYS_FILE_MAX_AGE,
        )
        self._uk_holidays.calendar_url = settings.UK_HOLIDAYS_SOURCE_URL

        self._days_manager = DayManager(uk_holidays=self._uk_holidays.calendar)

        self._make_alert_combinations()

    def clear(self):
        self._alert_combinations = {
            SEVERITY_STATUS.RED.name: {},
            SEVERITY_STATUS.AMBER.name: {},
            SEVERITY_STATUS.GREEN.name: {},
            SEVERITY_STATUS.CLEAN.name: {},
        }

        self._alert_sets = {
            SEVERITY_STATUS.RED.name: [],
            SEVERITY_STATUS.AMBER.name: [],
            SEVERITY_STATUS.GREEN.name: [],
            SEVERITY_STATUS.CLEAN.name: [],
        }
        self._test_data = {"repositories": [], "teams": [], "team_repositories": []}
        self._mock_scenarios = {}

    def __del__(self):
        self.clear()

    @property
    def alert_sets(self):
        return self._alert_sets

    @property
    def mock_scenarios(self):
        return self._mock_scenarios

    def _make_alert_combinations(self):

        self._alert_combinations[SEVERITY_STATUS.RED.name].update(
            {
                SEVERITY.CRITICAL.name: [EFFECTIVE_SEVERITY.CRITICAL_BREACH.name],
                SEVERITY.HIGH.name: [EFFECTIVE_SEVERITY.CRITICAL_BREACH.name],
                SEVERITY.MODERATE.name: [EFFECTIVE_SEVERITY.CRITICAL_BREACH.name],
                SEVERITY.LOW.name: [EFFECTIVE_SEVERITY.CRITICAL_BREACH.name],
            }
        )

        self._alert_combinations[SEVERITY_STATUS.AMBER.name].update(
            {
                SEVERITY.HIGH.name: [EFFECTIVE_SEVERITY.CRITICAL.name],
                SEVERITY.MODERATE.name: [
                    EFFECTIVE_SEVERITY.CRITICAL.name,
                    EFFECTIVE_SEVERITY.HIGH.name,
                ],
                SEVERITY.LOW.name: [
                    EFFECTIVE_SEVERITY.CRITICAL.name,
                    EFFECTIVE_SEVERITY.HIGH.name,
                    EFFECTIVE_SEVERITY.MODERATE.name,
                ],
            }
        )

        self._alert_combinations[SEVERITY_STATUS.GREEN.name].update(
            {
                SEVERITY.CRITICAL.name: [],
                SEVERITY.HIGH.name: [],
                SEVERITY.MODERATE.name: [],
                SEVERITY.LOW.name: [],
            }
        )

        self._alert_combinations[SEVERITY_STATUS.CLEAN.name].update({})

    def _make_name(self, length):
        """
        generate a randon name to be used for
         - alerts
         - teams
         - repositories
        """
        return "".join(random.choice(string.ascii_lowercase) for i in range(length))

    def _alert_template(
        self,
        severity,
        created_at,
        expected_fix_by,
        expected_effective_level,
        expected_age_in_business_days,
        expected_age_in_calendar_days,
    ):
        """
        Returns alerts structure as in schema. with expection of test_meta_data field
        test meta data contains
             - expected_effective_level
             - expected_fix_by_date
        We will use above two field to validate report

        Paramters:
        ----------
         - severity: str, original severity
         - created_at: date object, sets date of alert creation using back date method in DaysManager
         - expected_fix_by: test metadata object
         - expected_effective_level: test metadata object
        """
        return {
            "advisory_url": f"https://{self._make_name(length=5)}.com/{self._make_name(length=4)}",
            "createdAt": self._days_manager.date_to_str_datetime(date=created_at),
            "dismissedAt": None,
            "level": severity,
            "package": self._make_name(length=4),
            "patched_version": "X.Y.Z",
            "state": "OPEN",
            "test_expected_data": {
                "age_in_business_days": expected_age_in_business_days,
                "age_in_calendar_days": expected_age_in_calendar_days,
                "fix_by": self._days_manager.date_to_str_date(date=expected_fix_by),
                "effective_level": expected_effective_level,
            },
        }

    def _make_alert(self, original_severity, expected_severity, created_at):

        fix_by_business_days = ESCALATION_RULES[original_severity][
            EFFECTIVE_SEVERITY.CRITICAL_BREACH.name
        ]
        fix_by_calendar_days = self._days_manager.business_days_to_calendar_days(
            start_date=created_at, business_days=fix_by_business_days
        )

        fix_by = self._days_manager.end_date(
            start_date=created_at, calendar_days=fix_by_calendar_days
        )
        expected_age_in_business_days = self._days_manager.business_days_between(
            start_date=created_at
        )
        expected_age_in_calendar_days = self._days_manager.calendar_days_between(
            start_date=created_at
        )

        return self._alert_template(
            severity=original_severity,
            created_at=created_at,
            expected_fix_by=fix_by,
            expected_effective_level=expected_severity,
            expected_age_in_business_days=expected_age_in_business_days,
            expected_age_in_calendar_days=expected_age_in_calendar_days,
        )

    def create_alerts_set(self):
        for alert_status, combinaions in self._alert_combinations.items():
            """This is clean set"""
            if not combinaions:
                self.alert_sets[alert_status].append([])
            for original_severity, esclations in combinaions.items():
                """
                This is if we have GREEN severies with no escalation
                """
                if not esclations:
                    expected_severity = original_severity
                    days_to_avoid_escalation = TIME_TO_FIX[original_severity]
                    created_at = self._days_manager.date_before_n_business_days(
                        business_days=days_to_avoid_escalation
                    )

                    alert = self._make_alert(
                        original_severity=original_severity,
                        expected_severity=expected_severity,
                        created_at=created_at,
                    )
                    self._alert_sets[alert_status].append(alert)

                    continue

                """
                Only RED or AMBER will get here becasue,
                GREEN does not have any esclation points
                """
                for expected_severity in esclations:
                    days_to_avoid_escalation = ESCALATION_RULES[original_severity][
                        expected_severity
                    ]
                    days_to_esclate = days_to_avoid_escalation + 1
                    created_at = self._days_manager.date_before_n_business_days(
                        business_days=days_to_esclate
                    )
                    alert = self._make_alert(
                        original_severity=original_severity,
                        expected_severity=expected_severity,
                        created_at=created_at,
                    )
                    self._alert_sets[alert_status].append(alert)

    def generate_scenarios(self):

        """
        ----------------------
        |  | R | A | G | ORG |
        ----------------------
        | 1| x | x | x |  R  |
        | 2| x | x | C |  R  |
        | 3| x | C | x |  R  |
        | 4| x | C | C |  R  |
        | 5| C | x | x |  A  |
        | 6| C | x | C |  A  |
        | 7| C | C | x |  G  |
        | 8| C | C | C |  G  |
        ----------------------

        Scene Team 1 Team 2 Team 3 Team 4  OR G
         1      R    A        G      C      R
         2      R    A        C      C      R
         3      R    C        G      C      R
         4      R    C        C      C      R
         5      C    A        G      C      A
         6      C    A        C      C      A
         7      C    C        G      C      G
         8      C    C        C      C      C

        Team1 and, Repository 01 - 04   corrosponds to Column 1
        Team2 and, Repository 05 - 10   corrosponds to Column 2
        Team3 and, Repository 11 - 14   corrosponds to Column 3


        """

        self.SCENARIOS = {
            1: {
                "team1": {
                    "repositories": range(1, 5),
                    "status": SEVERITY_STATUS.RED.name,
                },
                "team2": {
                    "repositories": range(5, 11),
                    "status": SEVERITY_STATUS.AMBER.name,
                },
                "team3": {
                    "repositories": range(11, 15),
                    "status": SEVERITY_STATUS.GREEN.name,
                },
                "team4": {
                    "repositories": range(15, 16),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
            },
            2: {
                "team1": {
                    "repositories": range(1, 5),
                    "status": SEVERITY_STATUS.RED.name,
                },
                "team2": {
                    "repositories": range(5, 11),
                    "status": SEVERITY_STATUS.AMBER.name,
                },
                "team3": {
                    "repositories": range(11, 15),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team4": {
                    "repositories": range(15, 16),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
            },
            3: {
                "team1": {
                    "repositories": range(1, 5),
                    "status": SEVERITY_STATUS.RED.name,
                },
                "team2": {
                    "repositories": range(5, 11),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team3": {
                    "repositories": range(11, 15),
                    "status": SEVERITY_STATUS.GREEN.name,
                },
                "team4": {
                    "repositories": range(15, 16),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
            },
            4: {
                "team1": {
                    "repositories": range(1, 5),
                    "status": SEVERITY_STATUS.RED.name,
                },
                "team2": {
                    "repositories": range(5, 11),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team3": {
                    "repositories": range(11, 15),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team4": {
                    "repositories": range(15, 16),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
            },
            5: {
                "team1": {
                    "repositories": range(1, 5),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team2": {
                    "repositories": range(5, 11),
                    "status": SEVERITY_STATUS.AMBER.name,
                },
                "team3": {
                    "repositories": range(11, 15),
                    "status": SEVERITY_STATUS.GREEN.name,
                },
                "team4": {
                    "repositories": range(15, 16),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
            },
            6: {
                "team1": {
                    "repositories": range(1, 5),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team2": {
                    "repositories": range(5, 11),
                    "status": SEVERITY_STATUS.AMBER.name,
                },
                "team3": {
                    "repositories": range(11, 15),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team4": {
                    "repositories": range(15, 16),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
            },
            7: {
                "team1": {
                    "repositories": range(1, 5),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team2": {
                    "repositories": range(5, 11),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team3": {
                    "repositories": range(11, 15),
                    "status": SEVERITY_STATUS.GREEN.name,
                },
                "team4": {
                    "repositories": range(15, 16),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
            },
            8: {
                "team1": {
                    "repositories": range(1, 5),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team2": {
                    "repositories": range(5, 11),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team3": {
                    "repositories": range(11, 15),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
                "team4": {
                    "repositories": range(15, 16),
                    "status": SEVERITY_STATUS.CLEAN.name,
                },
            },
        }

        try:
            for index, scene_info in self.SCENARIOS.items():
                mock_data = {
                    "repositories": [],
                    "teams": list(scene_info.keys()),
                    "team_repositories": [],
                }

                for team, info in scene_info.items():
                    alerts = self.alert_sets[info["status"]]
                    team_repositories = []
                    for repo_index, repository_number in enumerate(
                        info["repositories"]
                    ):
                        repository_name = f"repository_{repository_number:02}"

                        mock_data["repositories"].append(
                            {
                                "name": repository_name,
                                "teams": [],
                                "topics": [settings.GITHUB_SKIP_SCAN_TOPIC]
                                if repo_index == 2
                                else [],
                                "alerts": [alerts[repo_index]]
                                if info["status"] != SEVERITY_STATUS.CLEAN.name
                                else [],
                            }
                        )
                        "skip adding 3rd repo to team to simulate orhpan repositories"
                        if repo_index != 3:
                            team_repositories.append(repository_name)
                    """
                    this part simulates token has no access i.e.
                     - Repository is not archived
                     - Team has Admin, maintainer or Write access on repo
                     - Token can not list it

                     It is added once for each team , so we should have 4 of these i.e. one per team
                    """
                    team_repositories.append(f"repository_{random.randrange(100,999)}")
                    mock_data["team_repositories"].append({team: team_repositories})

                """ validating mock data witch schema means,we have data in expected format"""
                scanner_data_schema.validate(mock_data)
                self._mock_scenarios.update({index: dict(mock_data)})
        except:
            raise


"""
These are helper functions
"""


def generate_mock_scenarios():
    """Generate json file with all scene"""
    mock_data = MockTestData()
    mock_data.create_alerts_set()
    mock_data.generate_scenarios()
    write_json_file(
        data=mock_data.mock_scenarios, dest_file=settings.TEST_SCENE_FILE_PATH
    )


def clear_mock_scenarios():
    "delete test scenes file"
    if settings.TEST_SCENE_FILE_PATH.exists():
        settings.TEST_SCENE_FILE_PATH.unlink()
