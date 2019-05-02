from django.contrib import admin

from github.models import GitHubTeam, GitHubRepo, GitHubVulnerabilityAlters, GitHubTeamRepo
# Register your models here.
@admin.register(GitHubTeam)
class GitHubTeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(GitHubRepo)
class GitHubRepoAdmin(admin.ModelAdmin):
    list_display = ('name', 'id')


@admin.register(GitHubVulnerabilityAlters)
class GitHubVulnerabilityAltersAdmin(admin.ModelAdmin):
    list_display = ('repository', 'critical', 'high', 'moderate', 'low')


@admin.register(GitHubTeamRepo)
class GitHubTeamRepoAdmin(admin.ModelAdmin):
    list_display = ('team', 'repository')
