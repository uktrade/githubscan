class ReportData:

    def __init__(self):
        pass

    def format(self, raw_report):
        repo_names = raw_report.keys()
        csv_data = list()
        email_content = str()
        data = dict()

        csv_data.append(["repository", "teams", "Package",
                         "Severity", "CVE", "CVE URL", "Github URL"])

        for repository in repo_names:
            critical_count = 0
            high_count = 0
            moderate_count = 0
            low_count = 0

            summary_string = str()

            severities = raw_report[repository]['severities']

            if raw_report[repository]['teams']:
                teams = "| ".join(raw_report[repository]['teams'])
            else:
                teams = 'None'

            severity_data = list()

            github_alerts_link = "https://github.com/uktrade/{}/network/alerts".format(
                repository)
            for severity in severities:
                severity_data = [repository, teams] + \
                    list(severity) + [github_alerts_link]

                if severity[1] == 'high':
                    high_count += 1
                if severity[1] == 'critical':
                    critical_count += 1
                if severity[1] == 'moderate':
                    moderate_count += 1
                if severity[1] == 'low':
                    low_count += 1

                if high_count or critical_count or moderate_count or low_count:
                    csv_data.append(severity_data)

                    email_content += "#{}\n * Critical: {} \n * High: {}\n * Moderate: {}\n * Low:{}\n * Associated team(s): {}\n * GitHub link: {} \n \n".format(
                        repository, critical_count, high_count, moderate_count, low_count, teams, github_alerts_link)

        data = {'csv': csv_data, 'content': email_content}

        return data
