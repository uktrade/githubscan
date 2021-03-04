
from django.conf import settings
from django.db.models import Q

from github.client import GHClient

from github.models import GitHubRepo
from github.models import GitHubTeam
from github.models import GitHubTeamRepo
from github.models import GitHubRepoVulnerabilites
from github.models import GitHubVulnerabilityCount

from github.db.retriver import Retriver


class Updater:

    def __init__(self):
        self.github_client = GHClient()
        self.skip_topic = settings.SKIP_TOPIC
        self.db_client = Retriver()

    def __repositories__(self):
        repositoriesInGitHub = self.github_client.getRepos()
        repositoriesInDb = self.db_client.getRepos()

        gitHubRepositoriesSet = set(repositoriesInGitHub)
        dbRepositoriesSet = set(
            repositoriesInDb.values_list('name', flat=True))

        add_records = gitHubRepositoriesSet.difference(dbRepositoriesSet)
        remove_records = dbRepositoriesSet.difference(gitHubRepositoriesSet)

        for record in remove_records:
            GitHubRepo.objects.filter(name=record).delete()

        for record in add_records:
            GitHubRepo(name=record).save()

    def __set_skip_scan__(self):
        repositoriesInDb = set(
            self.db_client.getRepos().values_list('name', flat=True))
        for repository in repositoriesInDb:
            topics = self.github_client.getRepoTopics(repository=repository)
            if topics:
                if self.skip_topic in topics:
                    GitHubRepo.objects.filter(
                        name=repository).update(skip_scan=True)

    def __teams__(self):
        teamsInGitHub = self.github_client.getTeams()
        teamsInDb = self.db_client.getTeams()

        gitHubTeamSet = set(teamsInGitHub)

        dbTeamSet = set(teamsInDb.values_list('name', flat=True))

        add_records = gitHubTeamSet.difference(dbTeamSet)
        remove_rcords = dbTeamSet.difference(gitHubTeamSet)

        for record in remove_rcords:
            GitHubTeam.objects.filter(name=record).delete()

        for record in add_records:
            GitHubTeam(name=record).save()

    def __teamRepositories__(self):
        # We don't need to remove team-repo association since it will be cascaded and removed

        teamsInDb = (self.db_client.getTeams()).values_list('name', flat=True)

        # Fetch repositories associated with each team
        for team in teamsInDb:
            teamRepositoriesInGitHub = self.github_client.getTeamRepos(
                team=team)
            teamRepositoriesInDb = self.db_client.getTeamRepos(team=team)

            gitHubTeamRepositoriesSet = set(teamRepositoriesInGitHub)
            dbTeamRepositoriesSet = set(
                teamRepositoriesInDb.values_list('repository', flat=True))

            add_records = gitHubTeamRepositoriesSet.difference(
                dbTeamRepositoriesSet)
            remove_records = dbTeamRepositoriesSet.difference(
                gitHubTeamRepositoriesSet)

            for repository in remove_records:
                GitHubTeamRepo.objects.filter(
                    team=self.db_client.getTeam(team=team), repository=self.db_client.getRepo(repository=repository)).delete()

            for repository in add_records:
                GitHubTeamRepo(team=self.db_client.getTeam(
                    team=team), repository=self.db_client.getRepo(repository=repository)).save()

    def __vulnerabilities__(self):

        # Drop it all before updating table
        GitHubRepoVulnerabilites.objects.all().delete()

        repositories = set(
            self.db_client.getRepos().values_list('name', flat=True))

        for repository in repositories:
            alertsInGithub = self.github_client.getVulnerabilityAlerts(
                repository=repository)
            if alertsInGithub:
                for alert in alertsInGithub:
                    GitHubRepoVulnerabilites(repository=self.db_client.getRepo(
                        repository=repository), package_name=alert[0], severity_level=alert[1], identifier_type=alert[2], identifier_value=alert[3], advisory_url=alert[4]).save()

    def __update_counts_(self):
        # Drop all before updating
        GitHubVulnerabilityCount.objects.all().delete()
        repositories = self.db_client.getVulnerableRepositories(
        ).values_list('repository', flat=True)

        for repository in repositories:
            repository_obj = self.db_client.getRepo(repository=repository)
            critical_count = GitHubRepoVulnerabilites.objects.filter(
                repository=repository_obj, severity_level='critical').count()
            high_count = GitHubRepoVulnerabilites.objects.filter(
                repository=repository_obj, severity_level='high').count()
            moderate_count = GitHubRepoVulnerabilites.objects.filter(
                repository=repository_obj, severity_level='moderate').count()
            low_count = GitHubRepoVulnerabilites.objects.filter(
                repository=repository_obj, severity_level='low').count()
            GitHubVulnerabilityCount(repository=repository_obj, critical=critical_count,
                                     high=high_count, moderate=moderate_count, low=low_count).save()

    def all(self):
        self.__repositories__()
        self.__set_skip_scan__()
        self.__teams__()
        self.__teamRepositories__()
        self.__vulnerabilities__()
        self.__update_counts_()
