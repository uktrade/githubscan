from github.helper.fetch.Github import Info
from github.helper.fetch.Db import Data
from github.models import GitHubTeam, GitHubRepo, GitHubVulnerabilityAlters, GitHubTeamRepo
from time import sleep
from django.conf import settings
from django.db.models import Q


class Update:

    def __init__(self):
        self.githubInfo = Info()
        self.dbData = Data()
        self.skip_topic = settings.SKIP_TOPIC

    def teams(self):
        teamsInGitHub = self.githubInfo.getTeams()
        teamsInDb = self.dbData.getTeams()

        gitHubTeamSet = set(teamsInGitHub)

        dbTeamSet = set(teamsInDb.values_list('name', flat=True))

        add_records = gitHubTeamSet.difference(dbTeamSet)
        remove_rcords = dbTeamSet.difference(gitHubTeamSet)

        for record in remove_rcords:
            GitHubTeam.objects.filter(name=record).delete()

        for record in add_records:
            GitHubTeam(name=record).save()

    def repostorties(self):
        repostortiesInGitHub = self.githubInfo.getRepos()
        repostortiesInDb = self.dbData.getRepos()

        gitHubRepositoriesSet = set(repostortiesInGitHub)
        dbRepositoriesSet = set(
            repostortiesInDb.values_list('name', flat=True))

        add_records = gitHubRepositoriesSet.difference(dbRepositoriesSet)
        remove_records = dbRepositoriesSet.difference(gitHubRepositoriesSet)

        # Add feature to remove record with the scan disabled

        for record in remove_records:
            GitHubRepo.objects.filter(name=record).delete()

        for record in add_records:
            GitHubRepo(name=record).save()

    def skip_scan(self):
        repostortiesInDb = set(
            self.dbData.getRepos().values_list('name', flat=True))

        for repository in repostortiesInDb:
            topics = self.githubInfo.getRepoTopics(repository=repository)
            skip_scan_status = False
            if topics:
                if self.skip_topic in topics:
                    skip_scan_status = True
            GitHubRepo.objects.filter(
                name=repository).update(skip_scan=skip_scan_status)

    def vulnerabilities(self):
        repostorties = set(
            self.dbData.getRepos().values_list('name', flat=True))

        # Remove repository vulnerability information which are Deleted or Archived
        currentRepositoriesInVulnerabilities = set(GitHubVulnerabilityAlters.objects.order_by(
            'repository').values_list('repository', flat=True).distinct())

        remove_repositoriesInVulnerabilities = currentRepositoriesInVulnerabilities.difference(
            repostorties)

        for repository in remove_repositoriesInVulnerabilities:
            GitHubVulnerabilityAlters.objects.filter(
                repository=repository).delete()

        # Remove all Repo with Zero Vulnurabilities
            GitHubVulnerabilityAlters.objects.filter(
                Q(critical__eq=0) & Q(high__eq=0) & Q(moderate__eq=0) & Q(low__eq=0))

        # Fetch and Update Vulnerabilities associated with each repo
        for repository in repostorties:
            alertsInGithub = self.githubInfo.getVulnerabilityAlerts(
                repository=repository)
            critical = alertsInGithub[repository]['critical']
            high = alertsInGithub[repository]['high']
            moderate = alertsInGithub[repository]['moderate']
            low = alertsInGithub[repository]['moderate']

            repo_exixts = GitHubVulnerabilityAlters.objects.filter(
                repository=repository).exists()

            # skip/delete if there are no severities
            if (critical == 0 and high == 0 and moderate == 0 and low == 0):
                if repo_exixts:
                    GitHubVulnerabilityAlters.objects.filter(
                        repository=repository).delete()
            else:
                if repo_exixts:
                    GitHubVulnerabilityAlters.objects.filter(repository=repository).update(
                        critical=critical, high=high, moderate=moderate, low=low)
                else:
                    GitHubVulnerabilityAlters(
                        repository=repository, critical=critical, high=high, moderate=moderate, low=low).save()

    def teamRepositories(self):
        teams = set(self.dbData.getTeams().values_list('name', flat=True))

        # Remove teams (and associated repositories) from team Repo which are deleted/renamed and do not exist on GitHub
        currentTeamsInTeamRepo = set(GitHubTeamRepo.objects.order_by(
            'team').values_list('team', flat=True).distinct())

        remove_teamsInTeamRepo = currentTeamsInTeamRepo.difference(teams)

        for team in remove_teamsInTeamRepo:
            GitHubTeamRepo.objects.filter(team=team).delete()

        # Fetch repositories associated with each team
        for team in teams:
            teamRepositoriesInGitHub = self.githubInfo.getTeamRepos(team=team)
            teamRepositoriesInDb = self.dbData.getTeamRepos(team=team)

            gitHubTeamRepositoriesSet = set(teamRepositoriesInGitHub)
            dbTeamRepositoriesSet = set(
                teamRepositoriesInDb.values_list('repository', flat=True))

            add_records = gitHubTeamRepositoriesSet.difference(
                dbTeamRepositoriesSet)
            remove_records = dbTeamRepositoriesSet.difference(
                gitHubTeamRepositoriesSet)

            for repository in add_records:
                GitHubTeamRepo(team=team, repository=repository).save()

            for repository in remove_records:
                GitHubTeamRepo.objects.filter(
                    team=team, repository=repository).delete()

    def all(self):
        self.teams()
        self.repostorties()
        self.skip_scan()
        self.vulnerabilities()
        self.teamRepositories()
