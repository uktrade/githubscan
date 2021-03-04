from github.models import GitHubRepo
from github.models import GitHubTeam
from github.models import GitHubTeamRepo
from github.models import GitHubRepoVulnerabilites
from github.models import GitHubVulnerabilityCount


class Retriver:

    def getRepos(self):
        return GitHubRepo.objects.all()

    def getTeams(self):
        return GitHubTeam.objects.all()

    def getTeamRepos(self, team):
        return GitHubTeamRepo.objects.filter(team=team)

    def getRepoTeams(self, repository):
        return GitHubTeamRepo.objects.filter(repository=repository)

    def getRepo(self, repository):
        return (self.getRepos()).filter(name=repository).first()

    def getTeam(self, team):
        return (self.getTeams()).filter(name=team).first()

    def getVulnerableRepositories(self):
        return GitHubRepoVulnerabilites.objects.values('repository').distinct()

    def getVulnerableRepoReport(self, repository):
        return GitHubVulnerabilityCount.objects.filter(repository=repository)

    def getSortedVunrableRepos(self, repositories):
        return GitHubVulnerabilityCount.objects.filter(repository__in=repositories).order_by('critical', 'high', 'moderate', 'low').reverse()

    def getDetailsRepoVulnerabilities(self, repository):
        return GitHubRepoVulnerabilites.objects.filter(repository=repository)
