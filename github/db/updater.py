
from django.conf import settings
from django.db.models import Q

from github.client import GHClient

from github.models import Repository
from github.models import Team

from github.models import RepositoryVulnerability
from github.models import RepositoryVulnerabilityCount
from github.models import RepositorySLOBreachCount
from github.models import TeamVulnerabilityCount

from github.db.retriver import Retriver
from datetime import datetime, timezone


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
            Repository.objects.filter(name=record).delete()

        for record in add_records:
            Repository(name=record).save()

    def __set_skip_scan__(self):
        repositoriesInDb = set(
            self.db_client.getRepos().values_list('name', flat=True))
        for repository in repositoriesInDb:
            topics = self.github_client.getRepoTopics(repository=repository)
            if topics:
                if self.skip_topic in topics:
                    Repository.objects.filter(
                        name=repository).update(skip_scan=True)

    def __teams__(self):
        teamsInGitHub = self.github_client.getTeams()
        teamsInDb = self.db_client.getTeams()

        gitHubTeamSet = set(teamsInGitHub)

        dbTeamSet = set(teamsInDb.values_list('name', flat=True))

        add_records = gitHubTeamSet.difference(dbTeamSet)
        remove_rcords = dbTeamSet.difference(gitHubTeamSet)

        for record in remove_rcords:
            Team.objects.filter(name=record).delete()

        for record in add_records:
            Team(name=record).save()

    def __teamRepositories__(self):
        # We don't need to remove team-repo association since it will be cascaded and removed

        teamsInDb = (self.db_client.getTeams()).values_list('name', flat=True)

        # Fetch repositories associated with each team and update

        for team in teamsInDb:
            teamRepositoriesInGitHub = set(self.github_client.getTeamRepos(
                team=team))

            teamRepositoriesInDB = set(self.db_client.getTeamRepos(
                team=team).repositories.values_list('name', flat=True))

            if teamRepositoriesInDB != teamRepositoriesInGitHub:
                Team(name=team).repositories.set(
                    teamRepositoriesInGitHub)

    def __vulnerabilities__(self):

        repositories = set(
            self.db_client.getRepos().values_list('name', flat=True))

        # collect active alerts per repo and delete non
        for repository in repositories:
            active_repo_alerts = []
            alertsInGithub = self.github_client.getVulnerabilityAlerts(
                repository=repository)
            if alertsInGithub:
                for alert in alertsInGithub:
                    package_name = alert[0]
                    severity_level = alert[1]
                    identifier_type = alert[2]
                    identifier_value = alert[3]
                    advisory_url = alert[4]
                    published_at = alert[5]
                    active_repo_alerts.append(
                        [repository, package_name, severity_level, identifier_type, identifier_value, advisory_url, published_at])

            # add/remove alerts
            alertsInDb = self.db_client.getDetailsRepoVulnerabilities(
                repository=repository)

            # if repo has active alert check if therre are new to add or have old to delete
            if active_repo_alerts:
                alertsSetInDb = set(alertsInDb.values_list('repository', 'package_name', 'severity_level',
                                                           'identifier_type', 'identifier_value', 'advisory_url', 'published_at'))
                alertsSetInGithub = set(tuple(row)
                                        for row in active_repo_alerts)

                add_records = alertsSetInGithub.difference(alertsSetInDb)
                remove_records = alertsSetInDb.difference(alertsSetInGithub)

                for record in remove_records:
                    alertsInDb.filter(repository=record[0], package_name=record[1], severity_level=record[2],
                                      identifier_type=record[3], identifier_value=record[4], advisory_url=record[5]).delete()

                for record in add_records:
                    RepositoryVulnerability(repository=self.db_client.getRepo(repository=record[0]), package_name=record[1], severity_level=record[
                                            2], identifier_type=record[3], identifier_value=record[4], advisory_url=record[5], published_at=record[6]).save()
            else:
                # if repo does not have any active alerts , delete it from record too
                alertsInDb.delete()

    def __update_vulnerability_age__(self):
        now = datetime.now(timezone.utc)
        for record in RepositoryVulnerability.objects.all():
            publish_age_in_days = (now - record.published_at).days
            detection_age_in_days = (now - record.detection_date).days
            RepositoryVulnerability.objects.filter(id=record.id).update(
                publish_age_in_days=publish_age_in_days, detection_age_in_days=detection_age_in_days)

    def __update_effective_servity_(self):
        max_critical_alert_age = 1
        max_high_alert_age = 7
        max_moderate_alert_age = 15

        for vulnerablity in RepositoryVulnerability.objects.all():

                #if detection age is more than lowest allowed age before it upgrades ( i.e. max_critical_alert_age  ) than do something!
                if vulnerablity.detection_age_in_days > max_critical_alert_age:
                    effective_severity_level = ''
                    #if original severity level is 'critical' it is a breach!
                    if vulnerablity.severity_level == 'critical':
                        effective_severity_level = 'SLA_BREACH'


                    if vulnerablity.severity_level == 'high':
                        if vulnerablity.detection_age_in_days > max_high_alert_age and vulnerablity.detection_age_in_days <= max_high_alert_age + max_critical_alert_age:
                            effective_severity_level = 'critical'
                        if vulnerablity.detection_age_in_days > max_high_alert_age + max_critical_alert_age:
                            effective_severity_level = 'SLA_BREACH'

                    if vulnerablity.severity_level == 'moderate':
                        if vulnerablity.detection_age_in_days > max_moderate_alert_age and vulnerablity.detection_age_in_days <= max_moderate_alert_age + max_high_alert_age:
                            effective_severity_level = 'high'
                        if vulnerablity.detection_age_in_days > max_moderate_alert_age + max_high_alert_age and vulnerablity.detection_age_in_days <= max_moderate_alert_age + max_high_alert_age + max_critical_alert_age:
                            effective_severity_level = 'critical'
                        if vulnerablity.detection_age_in_days > max_moderate_alert_age + max_high_alert_age + max_critical_alert_age:
                            effective_severity_level = 'SLA_BREACH'

                    #update effective severity level if it is not blank
                    if effective_severity_level:
                        RepositoryVulnerability.objects.filter(id=vulnerablity.id).update(effective_severity_level=effective_severity_level)

    def __update_slo_breach_status__(self):
        # Max alert accepable age in days
        # ref: https://readme.trade.gov.uk/docs/procedures/security-patching.html

        max_critical_alert_age = 1
        max_high_alert_age = 7
        max_moderate_alert_age = 15

        for critical_alert_record in RepositoryVulnerability.objects.filter(severity_level='critical').all():
            if critical_alert_record.publish_age_in_days > max_critical_alert_age:
                RepositoryVulnerability.objects.filter(
                    id=critical_alert_record.id).update(slo_breach=True)

        for high_alert_record in RepositoryVulnerability.objects.filter(severity_level='high').all():
            if high_alert_record.publish_age_in_days > max_high_alert_age:
                RepositoryVulnerability.objects.filter(
                    id=high_alert_record.id).update(slo_breach=True)

        for moderate_alert_record in RepositoryVulnerability.objects.filter(severity_level='moderate').all():
            if moderate_alert_record.publish_age_in_days > max_moderate_alert_age:
                RepositoryVulnerability.objects.filter(
                    id=moderate_alert_record.id).update(slo_breach=True)

    def __update_counts__(self):
        # Drop all before updating
        RepositoryVulnerabilityCount.objects.all().delete()
        repositories = self.db_client.getVulnerableRepositories(
        ).values_list('repository', flat=True)

        for repository in repositories:
            repository_obj = self.db_client.getRepo(repository=repository)
            critical_count = RepositoryVulnerability.objects.filter(
                repository=repository_obj, severity_level='critical').count()
            high_count = RepositoryVulnerability.objects.filter(
                repository=repository_obj, severity_level='high').count()
            moderate_count = RepositoryVulnerability.objects.filter(
                repository=repository_obj, severity_level='moderate').count()
            low_count = RepositoryVulnerability.objects.filter(
                repository=repository_obj, severity_level='low').count()

            effective_slabreach_count = RepositoryVulnerability.objects.filter(
                repository=repository_obj,effective_severity_level='SLA_BREACH').count()

            
            effective_critical_count = ( critical_count + RepositoryVulnerability.objects.filter(
                repository=repository_obj,effective_severity_level='critical').count() ) -  RepositoryVulnerability.objects.filter(
                repository=repository_obj,severity_level='critical',effective_severity_level='SLA_BREACH').count()


            effective_high_count = ( high_count + RepositoryVulnerability.objects.filter(
                repository=repository_obj,effective_severity_level='high').count() ) - (
                    RepositoryVulnerability.objects.filter(repository=repository_obj,severity_level='high',effective_severity_level='SLA_BREACH').count() +
                    RepositoryVulnerability.objects.filter(repository=repository_obj,severity_level='high',effective_severity_level='critical').count()                     
                )
          
            effective_moderate_count = ( moderate_count + RepositoryVulnerability.objects.filter(
                repository=repository_obj,effective_severity_level='moderate').count() ) - (
                    RepositoryVulnerability.objects.filter(repository=repository_obj,severity_level='moderate',effective_severity_level='SLA_BREACH').count() +
                    RepositoryVulnerability.objects.filter(repository=repository_obj,severity_level='moderate',effective_severity_level='critical').count() + 
                    RepositoryVulnerability.objects.filter(repository=repository_obj,severity_level='moderate',effective_severity_level='high').count()
                )

            effective_low_count = low_count - (
                    RepositoryVulnerability.objects.filter(repository=repository_obj,severity_level='low',effective_severity_level='SLA_BREACH').count() +
                    RepositoryVulnerability.objects.filter(repository=repository_obj,severity_level='low',effective_severity_level='critical').count() + 
                    RepositoryVulnerability.objects.filter(repository=repository_obj,severity_level='low',effective_severity_level='high').count() +
                    RepositoryVulnerability.objects.filter(repository=repository_obj,severity_level='low',effective_severity_level='moderate').count()
                )


            RepositoryVulnerabilityCount(repository=repository_obj, critical=critical_count,
                                         high=high_count, moderate=moderate_count, low=low_count,effective_slabreach=effective_slabreach_count,effective_critical=effective_critical_count,effective_high=effective_high_count,effective_moderate=effective_moderate_count,effective_low=effective_low_count).save()

    def __update_slo_breach_count__(self):

        # Clear table
        RepositorySLOBreachCount.objects.all().delete()

        breaches = RepositoryVulnerability.objects.filter(slo_breach=True)
        # if there are breaches
        if breaches:
            repositories = breaches.values_list(
                'repository', flat=True).distinct()

            for repository in repositories:
                repository_obj = self.db_client.getRepo(repository=repository)
                critical_count = breaches.filter(
                    repository=repository_obj, severity_level='critical').count()
                high_count = breaches.filter(
                    repository=repository_obj, severity_level='high').count()
                moderate_count = breaches.filter(
                    repository=repository_obj, severity_level='moderate').count()
                low_count = breaches.filter(
                    repository=repository_obj, severity_level='low').count()

                RepositorySLOBreachCount(repository=repository_obj, critical=critical_count,
                                         high=high_count, moderate=moderate_count, low=low_count).save()

    
    def __updat_team_vulnerability_count(self):
        # Clear table
        TeamVulnerabilityCount.objects.all().delete()

        teams = self.db_client.getTeams()

        for team in teams:
            team_repositories = set(self.db_client.getTeamRepos(team=team.name).repositories.all().values_list('name',flat=True))
            vulnerable_repositories = set(self.db_client.getVulnerableRepositories().values_list('repository',flat=True))
            repositories_of_interest = list(team_repositories.intersection(vulnerable_repositories))

            #if there is/are vulnerable repos
            if repositories_of_interest:
                critical_count = 0
                high_count = 0
                moderate_count = 0
                low_count = 0
                effective_slabreach_count = 0 
                effective_critical_count = 0
                effective_high_count = 0 
                effective_moderate_count = 0
                effective_low_count = 0 
                
                for repository in repositories_of_interest:
                    repository_report = self.db_client.getVulnerableRepoReport(repository=repository)
                    critical_count += repository_report.values_list('critical',flat=True)[0]
                    high_count +=repository_report.values_list('high',flat=True)[0]
                    moderate_count += repository_report.values_list('moderate',flat=True)[0]
                    low_count += repository_report.values_list('low',flat=True)[0]
                    effective_slabreach_count += repository_report.values_list('effective_slabreach',flat=True)[0]
                    effective_critical_count += repository_report.values_list('effective_critical',flat=True)[0]
                    effective_high_count += repository_report.values_list('effective_high',flat=True)[0]
                    effective_moderate_count += repository_report.values_list('effective_moderate',flat=True)[0]
                    effective_low_count += repository_report.values_list('effective_low',flat=True)[0]

                TeamVulnerabilityCount(team=team,critical=critical_count,high=high_count,moderate=moderate_count,low=low_count,effective_slabreach=effective_slabreach_count,effective_critical=effective_critical_count,effective_high=effective_high_count,effective_moderate=effective_moderate_count,effective_low=effective_low_count).save()





    def all(self):
        self.__repositories__()
        self.__set_skip_scan__()
        self.__teams__()
        self.__teamRepositories__()
        self.__vulnerabilities__()
        self.__update_vulnerability_age__()
        self.__update_effective_servity_()
        self.__update_slo_breach_status__()
        self.__update_counts__()
        self.__update_slo_breach_count__()
        self.__updat_team_vulnerability_count()