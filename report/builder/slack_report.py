# -*- coding: utf-8 -*-
from django.conf import settings

from common.functions import isinstance_of
from config.severities import EFFECTIVE_SEVERITY, SEVERITY
from report.helper.functions import sort_list_by_total


class BuildSlackReport:
    """
    Class to build a slack notification stack

    Variables:
    ----------
    self._slack_message , array of slack header and messages
    self.report_reader, ReportReder object instance
    """

    def __init__(self):
        self._slack_message = []
        self._slack_message_max_length = settings.SLACK_MESSAGE_LENGTH

    def clear(self):
        self._slack_message_max_length = settings.SLACK_MESSAGE_LENGTH
        self._slack_message.clear()

    def __del__(self):
        self.clear()

    def _add_slack_headr_and_message(self, header, section_text):
        """
        Set message header and message  in slack accepted format and,
        push it to the message array
        """
        isinstance_of(header, str, "header")
        isinstance_of(section_text, str, "section_text")

        message_header = {
            "type": "header",
            "text": {"type": "plain_text", "text": header},
        }

        message_section = {
            "type": "section",
            "text": {"type": "mrkdwn", "text": section_text},
        }

        self._slack_message.append(message_header)
        self._slack_message.append(message_section)

    @property
    def max_message_length(self):
        """
        Give max length of slack message
        set to settings.SLACK_MESSAGE_LENGTH ( 2800 chars) by default
        """
        return self._slack_message_max_length

    @max_message_length.setter
    def max_message_length(self, length):
        """
        Set max length of slack message
        """
        isinstance_of(length, int, "length")

        self._slack_message_max_length = length

    @property
    def slack_message(self):
        return self._slack_message

    @slack_message.setter
    def slack_message(self, message_data={}):
        """
        Create slack message array from message data
        """
        isinstance_of(message_data, dict, "message_data")

        if "header" not in message_data or "section" not in message_data:
            raise KeyError("header and section key must be present in data")

        isinstance_of(message_data["section"], list, 'message_data["section"]')

        if len(message_data.keys()) > 2:
            raise KeyError("only header and section key are expected")

        header = message_data["header"]

        """
        This loop can be improved to handle situation where
        first element of text itself is more the max_message_length
        however, for all practicle perpose we should never go beyond the
        max_message_length limit ( 2800 chars) on any of the array elemts
        """
        while message_data["section"]:
            section_text = "```"

            while (
                len(section_text) < self.max_message_length and message_data["section"]
            ):
                section_text += f'{message_data["section"].pop(0)}\n'

            section_text += "```"
            self._add_slack_headr_and_message(header=header, section_text=section_text)

            header = "-"

    def _section_text(self, total):
        """
        helper method to build section text with effective and original severities list
        """
        effective_severities = total["severities"]["effective"]
        original_severities = total["severities"]["original"]

        SECTION_TEXT_LIST = []

        SECTION_TEXT_LIST.append(
            f'{"Total Repositories:":22s}{total["repositories"]:3d}'
        )
        SECTION_TEXT_LIST.append(
            f'{"Total Critical Breach:":22s}{effective_severities[EFFECTIVE_SEVERITY.CRITICAL_BREACH.name]:3d}'
        )
        SECTION_TEXT_LIST.append(
            f'{"Total Critical:":22s}{original_severities[SEVERITY.CRITICAL.name]:3d} --> {"Effective Critical":20s}{effective_severities[EFFECTIVE_SEVERITY.CRITICAL.name]:3d}'
        )
        SECTION_TEXT_LIST.append(
            f'{"Total High:":22s}{original_severities[SEVERITY.HIGH.name]:3d} --> {"Effective High":20s}{effective_severities[EFFECTIVE_SEVERITY.HIGH.name]:3d}'
        )
        SECTION_TEXT_LIST.append(
            f'{"Total Moderate:":22s}{original_severities[SEVERITY.MODERATE.name]:3d} --> {"Effective Moderate":20s}{effective_severities[EFFECTIVE_SEVERITY.MODERATE.name]:3d}'
        )
        SECTION_TEXT_LIST.append(
            f'{"Total Low:":22s}{original_severities[SEVERITY.LOW.name]:3d} --> {"Effective High":20s}{effective_severities[EFFECTIVE_SEVERITY.LOW.name]:3d}'
        )

        return SECTION_TEXT_LIST

    def organization(self, report_reader):
        """
        get organization total
        """
        total = report_reader.organization_total

        HEADER_TEXT = "Github Organization Severity Report Summary"

        if total:
            SECTION_TEXT_LIST = self._section_text(total=total)
        else:
            SECTION_TEXT_LIST = ["all is well"]

        self.slack_message = {"header": HEADER_TEXT, "section": SECTION_TEXT_LIST}

    def unmonitored_repositories(self, report_reader):
        """
        Get skip scan repository report
        """
        total = report_reader.skip_scan_repositories["total"]

        HEADER_TEXT = "Github Unmonitored Repositories severity summary"

        if total["repositories"] >= 1:
            SECTION_TEXT_LIST = self._section_text(total=total)
        else:
            SECTION_TEXT_LIST = ["all is well"]

        self.slack_message = {"header": HEADER_TEXT, "section": SECTION_TEXT_LIST}

    def orphan_repositories(self, report_reader):
        """
        Get skip scan repository report
        """
        total = report_reader.orphan_repositories["total"]

        HEADER_TEXT = "Github Orphan Repositories severity summary"

        if total:
            SECTION_TEXT_LIST = self._section_text(total=total)
        else:
            SECTION_TEXT_LIST = ["all is well"]

        self.slack_message = {"header": HEADER_TEXT, "section": SECTION_TEXT_LIST}

    def organization_slo_breach(self, report_reader):
        """
        Get organization SLO breach
        """
        slo_breach = report_reader.organization_total["slo_breach"]

        slo_breach_severities = report_reader.organization_total["slo_breach"][
            "severities"
        ]

        HEADER_TEXT = "Github Organization SLO Breach report summary"

        SECTION_TEXT_LIST = []

        SECTION_TEXT_LIST.append(
            f'{"Total Repositories:":22s}{slo_breach["repositories"]:3d}'
        )
        SECTION_TEXT_LIST.append(
            f'{"Total Critical:":22s}{slo_breach_severities[SEVERITY.CRITICAL.name]:3d}'
        )
        SECTION_TEXT_LIST.append(
            f'{"Total High:":22s}{slo_breach_severities[SEVERITY.HIGH.name]:3d}'
        )
        SECTION_TEXT_LIST.append(
            f'{"Total Moderate:":22s}{slo_breach_severities[SEVERITY.MODERATE.name]:3d}'
        )
        SECTION_TEXT_LIST.append(
            f'{"Total Low:":22s}{slo_breach_severities[SEVERITY.LOW.name]:3d}'
        )

        if not SECTION_TEXT_LIST:
            SECTION_TEXT_LIST = ["all is well"]

        self.slack_message = {"header": HEADER_TEXT, "section": SECTION_TEXT_LIST}

    def teams(self, report_reader):
        reportable_teams = []
        for team in report_reader.processed_data["teams"].values():
            """
            Check if team have one or more vulnerable repositories
            """
            if team["total"]["repositories"] >= 1:
                reportable_teams.append(team)

        sorted_teams = sort_list_by_total(data=reportable_teams)

        HEADER_TEXT = "GitHub Teams Severity Report Summary"

        SECTION_TEXT_LIST = []

        if sorted_teams:
            SECTION_TEXT_LIST.append(f'{"Total Teams:":14s}{len(sorted_teams):3d}')

            for team in sorted_teams:
                original_severities = team["total"]["severities"]["original"]
                effective_severities = team["total"]["severities"]["effective"]

                team_name = f'{team["name"]}:'

                o_critical = original_severities[SEVERITY.CRITICAL.name]
                o_high = original_severities[SEVERITY.HIGH.name]
                o_moderate = original_severities[SEVERITY.MODERATE.name]
                o_low = original_severities[SEVERITY.LOW.name]

                e_critical_breach = effective_severities[
                    EFFECTIVE_SEVERITY.CRITICAL_BREACH.name
                ]
                e_critical = effective_severities[EFFECTIVE_SEVERITY.CRITICAL.name]
                e_high = effective_severities[EFFECTIVE_SEVERITY.HIGH.name]
                e_moderate = effective_severities[EFFECTIVE_SEVERITY.MODERATE.name]
                e_low = effective_severities[EFFECTIVE_SEVERITY.LOW.name]

                team_text = f"{team_name:42s}[{o_critical:2d},{o_high:2d},{o_moderate:2d},{o_low:2d}] --> [{e_critical_breach:2d},{e_critical:2d},{e_high:2d},{e_moderate:2d},{e_low:2d}]"
                SECTION_TEXT_LIST.append(team_text)
                team_text = ""

        else:
            SECTION_TEXT_LIST.append("all is well")

        self.slack_message = {"header": HEADER_TEXT, "section": SECTION_TEXT_LIST}

    def orphan_repositories_list(self, report_reader):
        orphan_repositories_list = report_reader.orphan_repositories["list"]

        HEADER_TEXT = "Github Organization Orphan Repositories list"

        SECTION_TEXT_LIST = []

        if orphan_repositories_list:
            SECTION_TEXT_LIST.append(
                f'{"Total Repositories:":20s}{len(orphan_repositories_list):3d}'
            )

            for repoistory_name in orphan_repositories_list:
                SECTION_TEXT_LIST.append(
                    f"* <https://github.com/uktrade/{repoistory_name}/settings/access | {repoistory_name}>"
                )
        else:
            SECTION_TEXT_LIST.append("all is well")
        self.slack_message = {"header": HEADER_TEXT, "section": SECTION_TEXT_LIST}

    def unmonitored_repositories_list(self, report_reader):
        """
        list of repositories with skip_scan set
        """
        skip_scan_repositories_list = report_reader.skip_scan_repositories["list"]

        HEADER_TEXT = "Github Unmonitored Repositories list"

        SECTION_TEXT_LIST = []

        if skip_scan_repositories_list:
            SECTION_TEXT_LIST.append(
                f'{"Total Repositories:":20s}{len(skip_scan_repositories_list):3d}'
            )
            for repoistory_name in skip_scan_repositories_list:
                SECTION_TEXT_LIST.append(
                    f"* <https://github.com/uktrade/{repoistory_name}/settings/access | {repoistory_name}>"
                )
        else:
            SECTION_TEXT_LIST.append("all is well")

        self.slack_message = {"header": HEADER_TEXT, "section": SECTION_TEXT_LIST}
