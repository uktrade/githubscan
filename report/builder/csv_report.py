# -*- coding: utf-8 -*-
from report.helper.functions import sort_list_by_total, sort_alerts_list
from config.severities import EFFECTIVE_SEVERITY
from pathlib import Path, PosixPath
from common.functions import isinstance_of
from config.date_formats import DATE_FORMAT
from datetime import datetime
import csv


class BuildCSVReport:
    """
    create csv report file for organization and team
    """

    def __init__(self):
        self._root_path = Path(__file__).parent.parent.parent

    def clear(self):
        pass

    def organization_report(self, report_reader):
        file_path = Path.joinpath(self._root_path, "organization_report.csv")

        csv_data = self._make_csv_data_(
            repositories_list=report_reader.reportable_organization_repositories_list
        )

        self._write_csv_file_(path=file_path, csv_content=csv_data)

        return file_path

    def team_report(self, team, report_reader):

        file_path = Path.joinpath(self._root_path, f"{team}.csv")

        csv_data = self._make_csv_data_(
            repositories_list=report_reader.reportable_team_repositories_list(
                team=team
            ),
            team=team,
        )

        self._write_csv_file_(path=file_path, csv_content=csv_data)

        return file_path

    def _make_csv_data_(self, repositories_list, team=None):
        """
        Build csv compitable list
        """
        isinstance_of(repositories_list, list, "repositories_list")

        csv_content = []
        csv_content.append(
            [
                "Repository",
                "Team(s)",
                "Created At",
                "Package",
                "Severity",
                "Effective Severity",
                "Critical Breach",
                "age_in_business_days",
                "age_in_calendar_days",
                "Advisory Link",
                "Github Alerts Link",
            ]
        )

        for repository in sort_list_by_total(repositories_list):
            for alert in sort_alerts_list(repository["alerts"]):
                created_at = datetime.strftime(
                    datetime.strptime(
                        alert["createdAt"], DATE_FORMAT.DATE_TIME.value
                    ).date(),
                    DATE_FORMAT.DATE.value,
                )
                csv_content.append(
                    [
                        repository["name"],
                        team if team else f'{"|".join(repository["teams"])}',
                        created_at,
                        alert["package"],
                        alert["level"],
                        alert["effective_level"],
                        True
                        if alert["effective_level"]
                        == EFFECTIVE_SEVERITY.CRITICAL_BREACH.name
                        else False,
                        alert["age_in_business_days"],
                        alert["age_in_calendar_days"],
                        alert["advisory_url"],
                        f'https://github.com/uktrade/{repository["name"]}/network/alerts',
                    ]
                )

        return csv_content

    def _write_csv_file_(self, path, csv_content):
        """
        write csv file
        """
        isinstance_of(path, PosixPath, "path")
        isinstance_of(csv_content, list, "csv_content")

        try:
            with open(path, "w") as csv_file:
                f = csv.writer(csv_file)
                f.writerows(csv_content)
                csv_file.close()
        except:
            raise
