from github.models import GitHubRepo, GitHubTeam, GitHubVulnerabilityAlters, GitHubTeamRepo


class Data:

    def getTeams(self):
        teams = GitHubTeam.objects.all()
        return teams

    def getRepos(self):
        repositories = GitHubRepo.objects.all()
        return repositories

    def getVulnerabilities(self, repository):
        vulnerabilities = GitHubVulnerabilityAlters.objects.filter(
            repository=repository)
        return vulnerabilities

    def getTeamRepos(self, team):
        teamrepos = GitHubTeamRepo.objects.filter(team=team)
        return teamrepos

    def getRepoteams(self, repository):
        repoteams = GitHubTeamRepo.objects.filter(repository=repository)
        return repoteams
