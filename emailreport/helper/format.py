from tabulate import tabulate


class ReportData:

    def __init__(self):
        pass

    def format(self, raw_report):
        names = raw_report.keys()
        data = list()

        for name in names:
            severities = raw_report[name]['severities']
            teams = raw_report[name]['teams']
            severity_data = list()
            team = str()
            github_alerts_link = "https://github.com/uktrade/{}/network/alerts".format(
                name)
            for index, severity in enumerate(severities):
                if len(teams):
                    team = teams.pop()
                if index is 0:
                    if not team:
                        team = 'None'
                    severity_data = [
                        name, team] + list(severity) + [github_alerts_link]
                else:
                    severity_data = ['', team] + list(severity) + ['']
                team = str()
                data.append(severity_data)

            if len(teams):
                for team in teams:
                    severity_data = ['', team, '', '', '', '', '']
                    data.append(severity_data)

        return tabulate(data, headers=[
            "repository", "teams", "Package", "Severity", "CVE", "CVE URL", "Github URL"], tablefmt="grid")
