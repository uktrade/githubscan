from github.helper.fetch.Github import Info
from github.helper.fetch.Db import Data
from github.models import GitHubTeam, GitHubRepo, GitHubVulnerabilityAlters, GitHubTeamRepo
from time import sleep


class Update:

    def __init__(self):
        self.githubInfo = Info()
        self.dbData = Data()

    def teams(self):
        teamsInGitHub = self.githubInfo.getTeams()
        teamsInDb = self.dbData.getTeams()

        gitHubTeamSet = set(teamsInGitHub.keys())
        dbTeamSet = set(teamsInDb.values_list('id', flat=True))

        add_records = gitHubTeamSet.difference(dbTeamSet)
        remove_rcords = dbTeamSet.difference(gitHubTeamSet)

        for id in add_records:
            GitHubTeam(id=id, name=teamsInGitHub[id]).save()

        for id in remove_rcords:
            GitHubTeam.objects.filter(id=id).delete()

    def repostorties(self):
        repostortiesInGitHub = self.githubInfo.getRepos()
        repostortiesInDb = self.dbData.getRepos()

        gitHubRepositoriesSet = set(repostortiesInGitHub.keys())
        dbRepositoriesSet = set(repostortiesInDb.values_list('id', flat=True))

        add_record = gitHubRepositoriesSet.difference(dbRepositoriesSet)
        remove_record = dbRepositoriesSet.difference(gitHubRepositoriesSet)

        for id in add_record:
            GitHubRepo(id=id, name=repostortiesInGitHub[id]).save()

        for id in remove_record:
            GitHubRepo.objects.filter(id=id).delete()

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

        # Fetch and Update Vulnerabilities associated with each repo
        for repository in repostorties:
            alertsInGithub = self.githubInfo.getVulnerabilityAlerts(
                repository=repository)
            critical = alertsInGithub[repository]['critical']
            high = alertsInGithub[repository]['high']
            moderate = alertsInGithub[repository]['moderate']
            low = alertsInGithub[repository]['moderate']

            GitHubVulnerabilityAlters.objects.update_or_create(
                repository=repository, critical=critical, high=high, moderate=moderate, low=low)

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
        self.vulnerabilities()
        self.teamRepositories()
