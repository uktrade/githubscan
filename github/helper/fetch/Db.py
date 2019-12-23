from django.db.models import Q
from github.models import GitHubRepo, GitHubTeam, GitHubVulnerabilityAlters, GitHubTeamRepo


class Data:

    def getTeams(self):
        teams = GitHubTeam.objects.all()
        return teams

    def getTeamAdminEmails(self):
        return self.getTeams().exclude(admin_email='').values('admin_email').distinct()

    def getTeamsByAdminEmail(self,admin_email):
        return self.getTeams().filter(admin_email=admin_email)

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

    def getTeamAdminEmail(self, team):
        admin_email = str()
        admin_email = (GitHubTeam.objects.filter(
            team=team).values_list('admin_email', flat=True))[0]
        return admin_email
