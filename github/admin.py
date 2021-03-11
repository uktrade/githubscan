from django.contrib import admin

from github.models import Repository
from github.models import Team
from github.models import RepositoryVulnerabilityCount
from github.models import RepositoryVulnerability
from github.models import RepositorySLOBreachCount
# Register your models here.


@admin.register(Repository)
class GitHubRepoAdmin(admin.ModelAdmin):
    list_display = ('name', 'skip_scan')


@admin.register(Team)
class GitHubTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(RepositoryVulnerabilityCount)
class GitHubVulnerabilityCountAdmin(admin.ModelAdmin):
    list_display = ('repository', 'critical', 'high', 'moderate', 'low')


@admin.register(RepositoryVulnerability)
class GitHubRepoVulnerabilitesAdmin(admin.ModelAdmin):
    list_display = ('repository', 'identifier_type',
                    'identifier_value', 'severity_level', 'advisory_url')


@admin.register(RepositorySLOBreachCount)
class GitHubSloBreachCountAdmin(admin.ModelAdmin):
    list_display = ('repository', 'critical', 'high', 'moderate', 'low')
