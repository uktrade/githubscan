from github.models import Repository
from github.models import Team
from github.models import RepositoryVulnerability
from github.models import RepositoryVulnerabilityCount
from github.models import RepositorySLOBreachCount
from github.models import TeamVulnerabilityCount


class Retriver:

    def getRepos(self):
        return Repository.objects.all()

    def getTeams(self):
        return Team.objects.all()

    def getTeamRepos(self, team):
        return Team(name=team)

    def getRepoTeams(self, repository):
        # This is how you retrive all the team for repository in many to many realtion
        return Team.objects.filter(repositories__name=repository)

    def getRepo(self, repository):
        return Repository(name=repository)

    def getTeam(self, team):
        return (self.getTeams()).filter(name=team).first()

    def getVulnerableRepositories(self):
        return RepositoryVulnerability.objects.values('repository').distinct()

    def getVulnerableRepoReport(self, repository):
        return RepositoryVulnerabilityCount.objects.filter(repository=repository)

    def getSortedVunrableRepos(self, repositories):
        return RepositoryVulnerabilityCount.objects.filter(repository__in=repositories).order_by('effective_slabreach', 'critical', 'high', 'moderate', 'low').reverse()

    def getDetailsRepoVulnerabilities(self, repository):
        return RepositoryVulnerability.objects.filter(repository=repository)

    def getRepoSloBreach(self, repository):
        return RepositorySLOBreachCount.objects.filter(repository=repository)

    def getSloBreachRepos(self):
        return RepositorySLOBreachCount.objects.all()

    def getSloBreachReposOfInterest(self, repositories):
        return RepositorySLOBreachCount.objects.filter(repository__in=repositories)

    def getSortedTeamsVulnerabilitySummaryReport(self):
        return TeamVulnerabilityCount.objects.order_by('critical', 'high', 'moderate', 'low').reverse()
