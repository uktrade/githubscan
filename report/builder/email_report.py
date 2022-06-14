# -*- coding: utf-8 -*-
from report.helper.functions import sort_list_by_total, sort_alerts_list
from config.severities import SEVERITY_STATUS, EFFECTIVE_SEVERITY, SEVERITY


class BuildEmailReport:
    """ "
    Format and send out emails desired receiver:
    """

    def __init__(self):
        pass

    def clear(self):
        pass

    def organization_summary(self, report_reader):
        """
        send org level summary report
        """

        email_report = {}

        total = report_reader.organization_total

        severity_status = (
            SEVERITY_STATUS.GREEN.name
            if report_reader.organization_severity_status == SEVERITY_STATUS.CLEAN.name
            else report_reader.organization_severity_status
        )

        email_report = self._format_summary_email(
            severity_status=severity_status,
            repositories_list=report_reader.reportable_organization_repositories_list,
            total=total,
        )

        email_report.update({"severity_status": severity_status})

        email_report.update(
            {
                "subject": f"[{severity_status}] Daily: Github Organisation Vulnerabilities Scan Report"
            }
        )
        return email_report

    def organization_detailed(self, report_reader):
        """
        send org level details
        """

        email_report = {}

        severity_status = (
            SEVERITY_STATUS.GREEN.name
            if report_reader.organization_severity_status == SEVERITY_STATUS.CLEAN.name
            else report_reader.organization_severity_status
        )

        email_report = self._format_detailed_repository_report(
            repositories_list=report_reader.reportable_organization_repositories_list
        )

        email_report.update(
            {
                "subject": f'{email_report["action_by"]} {email_report["vulnerable_packages"]} Vulnerable packages Detailed Organization report'
            }
        )

        email_report.update({"severity_status": severity_status})

        return email_report

    def teams_summary(self, team, report_reader):

        if team not in report_reader.teams:
            raise ValueError(f"Uknown Team:{team}")

        email_report = {}

        team_report_total = report_reader.teams[team]["total"]
        team_severity_status = (
            SEVERITY_STATUS.GREEN.name
            if report_reader.teams[team]["severity_status"]
            == SEVERITY_STATUS.CLEAN.name
            else report_reader.teams[team]["severity_status"]
        )

        email_report = self._format_summary_email(
            severity_status=team_severity_status,
            repositories_list=report_reader.reportable_team_repositories_list(
                team=team
            ),
            total=team_report_total,
        )

        email_report.update(
            {
                "subject": f"[{team_severity_status}] Daily: Github {team.capitalize()} team Vulnerabilities Scan Report"
            }
        )

        email_report.update({"severity_status": team_severity_status})

        return email_report

    def team_detailed(self, team, report_reader):
        """
        send team level details
        """

        email_report = {}

        if team not in report_reader.teams:
            raise ValueError("Uknown Team:{tean}")

        team_severity_status = (
            SEVERITY_STATUS.GREEN.name
            if report_reader.teams[team]["severity_status"]
            == SEVERITY_STATUS.CLEAN.name
            else report_reader.teams[team]["severity_status"]
        )

        email_report = self._format_detailed_repository_report(
            repositories_list=report_reader.reportable_team_repositories_list(team=team)
        )

        email_report.update(
            {
                "subject": f'{email_report["action_by"]} {email_report["vulnerable_packages"]} Vulnerable packages - {team.capitalize()} Github report'
            }
        )

        email_report.update({"severity_status": team_severity_status})

        return email_report

    def _format_summary_email(self, severity_status, repositories_list, total):

        sorted_repositories = sort_list_by_total(repositories_list)

        formatted_total = self._format_total(total=total)

        TOTAL_REPOSITORIES_TEXT = (
            f'{"total Repositories:":20s} {total["repositories"]:3d}'
        )

        TOTAL_SLO_BREACH_REPOSITORIES_TEXT = (
            f'{"total Repositories:":20s} {total["slo_breach"]["repositories"]:3d}'
        )

        REPORT_RATING_TEXT = ["#Report Rating", severity_status]

        VULNERABILITY_SUMMARY_TEXT = [
            "#Vulnerability Summary",
            TOTAL_REPOSITORIES_TEXT,
            formatted_total["TOTAL_CRITICAL_BREACH_TEXT"],
            formatted_total["TOTAL_CRITICAL_ALERT_TEXT"],
            formatted_total["TOTAL_HIGH_ALERT_TEXT"],
            formatted_total["TOTAL_MODERATEL_ALERT_TEXT"],
            formatted_total["TOTAL_LOW_ALERT_TEXT"],
        ]

        SLO_BREACH_SUMMARY_TEXT = [
            "#SLO Breach Summary",
            TOTAL_SLO_BREACH_REPOSITORIES_TEXT,
            formatted_total["TOTAL_SLO_BREACH_CRITIAL_TEXT"],
            formatted_total["TOTAL_SLO_BREACH_HIGH_TEXT"],
            formatted_total["TOTAL_SLO_BREACH_MODERATE_TEXT"],
            formatted_total["TOTAL_SLO_BREACH_LOW_TEXT"],
        ]

        SUMMARY_TEXT = (
            REPORT_RATING_TEXT
            + [""]
            + VULNERABILITY_SUMMARY_TEXT
            + [""]
            + SLO_BREACH_SUMMARY_TEXT
        )

        REPOSITORY_SUMMARY_TEXT = []

        for repository in sorted_repositories:
            formatted_total = self._format_total(total=repository["total"])
            REPOSITORY_SUMMARY_TEXT.append(f'#{repository["name"]}')
            REPOSITORY_SUMMARY_TEXT.append(
                formatted_total["TOTAL_CRITICAL_BREACH_TEXT"]
            )
            REPOSITORY_SUMMARY_TEXT.append(formatted_total["TOTAL_CRITICAL_ALERT_TEXT"])
            REPOSITORY_SUMMARY_TEXT.append(formatted_total["TOTAL_HIGH_ALERT_TEXT"])
            REPOSITORY_SUMMARY_TEXT.append(
                formatted_total["TOTAL_MODERATEL_ALERT_TEXT"]
            )
            REPOSITORY_SUMMARY_TEXT.append(formatted_total["TOTAL_LOW_ALERT_TEXT"])
            REPOSITORY_SUMMARY_TEXT.append(
                f'* {"Associated team(s):":20s} {",".join(repository["teams"])}'
            )
            REPOSITORY_SUMMARY_TEXT.append(
                f'* GitHub link: https://github.com/uktrade/{repository["name"]}/network/alerts'
            )
            REPOSITORY_SUMMARY_TEXT.append("")
            REPOSITORY_SUMMARY_TEXT.append(f"SLO Breaches")
            REPOSITORY_SUMMARY_TEXT.append(
                formatted_total["TOTAL_SLO_BREACH_CRITIAL_TEXT"]
            )
            REPOSITORY_SUMMARY_TEXT.append(
                formatted_total["TOTAL_SLO_BREACH_HIGH_TEXT"]
            )
            REPOSITORY_SUMMARY_TEXT.append(
                formatted_total["TOTAL_SLO_BREACH_MODERATE_TEXT"]
            )
            REPOSITORY_SUMMARY_TEXT.append(formatted_total["TOTAL_SLO_BREACH_LOW_TEXT"])
            REPOSITORY_SUMMARY_TEXT.append("")

        return {
            "content": "\n".join(REPOSITORY_SUMMARY_TEXT),
            "summary": "\n".join(SUMMARY_TEXT),
        }

    def _format_total(self, total):

        return {
            "TOTAL_CRITICAL_BREACH_TEXT": f'{"* total Effective Critical Breach:":29s}{total["severities"]["effective"][EFFECTIVE_SEVERITY.CRITICAL_BREACH.name]:3d}',
            "TOTAL_CRITICAL_ALERT_TEXT": f'{"* total CRITICAL:":20s}{total["severities"]["original"][SEVERITY.CRITICAL.name]:3d} ---> {"total Effective Critical:":20s} {total["severities"]["effective"][EFFECTIVE_SEVERITY.CRITICAL.name]:3d}',
            "TOTAL_HIGH_ALERT_TEXT": f'{"* total HIGH:":20s} {total["severities"]["original"][SEVERITY.HIGH.name]:3d} ---> {"total Effective Hight:":20s} {total["severities"]["effective"][EFFECTIVE_SEVERITY.HIGH.name]:3d}',
            "TOTAL_MODERATEL_ALERT_TEXT": f'{"* total MODERATE:":20s}{total["severities"]["original"][SEVERITY.MODERATE.name]:3d} ---> {"total Effective Moderate:":20s} {total["severities"]["effective"][EFFECTIVE_SEVERITY.MODERATE.name]:3d}',
            "TOTAL_LOW_ALERT_TEXT": f'{"* total LOW:":20s} {total["severities"]["original"][SEVERITY.LOW.name]:3d} ---> {"total Effective Low:":20s} {total["severities"]["effective"][EFFECTIVE_SEVERITY.LOW.name]:3d}',
            "TOTAL_SLO_BREACH_CRITIAL_TEXT": f'{"* total Critical:":20s} {total["slo_breach"]["severities"][SEVERITY.CRITICAL.name]:3d}',
            "TOTAL_SLO_BREACH_HIGH_TEXT": f'{"* total High:":20s} {total["slo_breach"]["severities"][SEVERITY.HIGH.name]:3d}',
            "TOTAL_SLO_BREACH_MODERATE_TEXT": f'{"* total Moderate:":20s} {total["slo_breach"]["severities"][SEVERITY.MODERATE.name]:3d}',
            "TOTAL_SLO_BREACH_LOW_TEXT": f'{"* total Low:":20s} {total["slo_breach"]["severities"][SEVERITY.LOW.name]:3d}',
        }

    def _format_detailed_repository_report(self, repositories_list):

        alerts_list = []
        alerts_repo = {}
        sorted_alerts = []

        """
        This part ensures, we get only uniq alerts in the alerts list and,
        we add repsitory in the list
        """
        for repository in repositories_list:
            for alert in repository["alerts"]:
                if alert["hash"] not in alerts_repo.keys():
                    alerts_repo.update(
                        {
                            alert["hash"]: {
                                "package": alert["package"],
                                "repositories": [repository["name"]],
                            }
                        }
                    )
                    alerts_list.append(alert)
                    continue

                alerts_repo[alert["hash"]]["repositories"].append(repository["name"])

        sorted_alerts = sort_alerts_list(data=alerts_list)

        ALERT_DETAIL_TEXT = []
        action_by = ""
        vulnerable_packages = len(sorted_alerts)

        if sorted_alerts:
            action_by = f'[Action by: {sorted_alerts[0]["fix_by"]}]'

        for alert in sorted_alerts:
            REPOSITORY_TEXT = []

            for repository_name in alerts_repo[alert["hash"]]["repositories"]:
                REPOSITORY_TEXT.append(
                    f" * {repository_name} https://github.com/uktrade/{repository_name}/security/dependabot"
                )

            ALERT_DETAIL_TEXT += [
                f'#{alert["package"]}',
                f'{"Patch by:":10s} {alert["fix_by"]:10s} ({alert["days_to_fix"]:3d} days)',
                f'* {"Patched version":20s} {alert["patched_version"]}',
                f'* {"Effective severity:":20s} {alert["effective_level"]}',
                f'* {"Original severity:":20s} {alert["level"]}',
                f'* {"Advisory":20s} {alert["advisory_url"]}',
                f'* {"Repositories"}',
                "\n".join(set(REPOSITORY_TEXT)),
                "",
            ]

        return {
            "action_by": action_by,
            "vulnerable_packages": vulnerable_packages,
            "content": "\n".join(ALERT_DETAIL_TEXT),
        }
