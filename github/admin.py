from django.contrib import admin

from github.models import GitHubTeam, GitHubRepo, GitHubVulnerabilityAlters, GitHubTeamRepo, GitHubTeamAdminEmail
# Register your models here.
@admin.register(GitHubTeam)
class GitHubTeamAdmin(admin.ModelAdmin):
    pass


@admin.register(GitHubRepo)
class GitHubRepoAdmin(admin.ModelAdmin):
    pass


@admin.register(GitHubVulnerabilityAlters)
class GitHubVulnerabilityAltersAdmin(admin.ModelAdmin):
    list_display = ('repository', 'critical', 'high', 'moderate', 'low')


@admin.register(GitHubTeamRepo)
class GitHubTeamRepoAdmin(admin.ModelAdmin):
    list_display = ('team', 'repository')


@admin.register(GitHubTeamAdminEmail)
class GitHibTeamAdminEmailAdmin(admin.ModelAdmin):
    list_display = ('team', 'admin_email')
