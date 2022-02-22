from github.db.retriver import Retriver


class Report:
    def __init__(self):
        self.db_client = Retriver()

    def getReportRepos(self):
        repositories = set(
            (self.db_client.getRepos())
            .filter(skip_scan=False)
            .values_list("name", flat=True)
        )
        reported_repositories = set(
            self.db_client.getVulnerableRepositories().values_list(
                "repository", flat=True
            )
        )
        return repositories.intersection(reported_repositories)

    def getSkippedRepos(self):
        repositories = set(
            (self.db_client.getRepos())
            .filter(skip_scan=True)
            .values_list("name", flat=True)
        )
        reported_repositories = set(
            self.db_client.getVulnerableRepositories().values_list(
                "repository", flat=True
            )
        )
        return repositories.intersection(reported_repositories)

    def getTeamReportRepos(self, team):
        """Returns all of this team's "reportable" repos (not part of the
        "default" team's repos and not flagged for skipping) that have a
        vulnerability.
        """

        # Retrieve the team's repositories.
        team_repositories = set(
            self.db_client.getTeamRepos(team=team).repositories.values_list(
                "name", flat=True
            )
        )

        # If team is not "default", then remove the "default" team's
        # repositories from this team's set of reported-on repos.
        if team != "default":
            default_team_repositories = set(
                self.db_client.getTeamRepos(team="default").repositories.values_list(
                    "name", flat=True
                )
            )
            team_repositories = team_repositories.difference(default_team_repositories)

        # Retrieve all actively scanned repos - i.e. those not flagged as
        # "skip_scan=True".
        repositories = set(
            (self.db_client.getRepos())
            .filter(skip_scan=False)
            .values_list("name", flat=True)
        )

        # Retrieve all repositories that have a vulnerability.
        reported_repositories = set(
            self.db_client.getVulnerableRepositories().values_list(
                "repository", flat=True
            )
        )

        # Return all of this team's reportable repos that have a vulnerability.
        return (repositories.intersection(reported_repositories)).intersection(
            team_repositories
        )
