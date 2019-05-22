from github.models import GitHubRepo, GitHubTeam, GitHubVulnerabilityAlters, GitHubTeamRepo


class Data:

    def getTeams(self):
        teams = GitHubTeam.objects.all()
        return teams

    def getRepos(self):
        repositories = GitHubRepo.objects.filter(skip_scan=False)
        return repositories

    def getVulnerabilities(self, repository):
        vulnerabilities = GitHubVulnerabilityAlters.objects.filter(
            repository=repository)
        return vulnerabilities

    def getAllVulnerabilities(self):
        vulnerabilities = GitHubVulnerabilityAlters.objects.all()
        return vulnerabilities

    def getTeamRepos(self, team):
        teamrepos = GitHubTeamRepo.objects.filter(team=team)
        return teamrepos

    def getRepoteams(self, repository):
        repoteams = GitHubTeamRepo.objects.filter(repository=repository)
        return repoteams
