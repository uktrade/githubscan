from django.db.models import Q
from github.models import GitHubRepo, GitHubTeam, GitHubVulnerabilityAlters, GitHubTeamRepo, GitHubTeamAdminEmail


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

    def getVulnerableRepos(self):
        vulnerableRepos = GitHubVulnerabilityAlters.objects.values_list(
            'repository', flat=True)
        return vulnerableRepos

    def getTeamsFromAdminTable(self):
        teamsInAdminTable = GitHubTeamAdminEmail.objects.values_list(
            'team', flat=True)
        return teamsInAdminTable

    def getTeamAdminEmail(self, team):
        admin_email = str()
        admin_email = (GitHubTeamAdminEmail.objects.filter(
            team=team).values_list('admin_email', flat=True))[0]
        return admin_email
