from collections import Counter


class ReportData:

    def __init__(self):
        pass

    def format(self, raw_report):
        repo_names = raw_report.keys()
        csv_data = list()
        email_content = ''
        data = dict()
        severity_counter = Counter()
        csv_data.append(["repository", "teams", "Package",
                         "Severity", "CVE", "CVE URL", "Github URL"])

        for repository in repo_names:

            summary_string = ''

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

                severity_counter[severity[1]] += 1

            if(list(severity_counter.elements())):
                csv_data.append(severity_data)
                email_content += "#{}\n * Critical: {} \n * High: {}\n * Moderate: {}\n * Low:{}\n * Associated team(s): {}\n * GitHub link: {} \n \n".format(
                    repository, severity_counter['critical'], severity_counter['high'], severity_counter['moderate'], severity_counter['low'], teams, github_alerts_link)
                severity_counter.clear()

        data = {'csv': csv_data, 'content': email_content}

        return data
