from django.contrib import admin

from github.models import GitHubRepo
from github.models import GitHubTeam
from github.models import GitHubTeamRepo
from github.models import GitHubVulnerabilityCount
from github.models import GitHubRepoVulnerabilites

# Register your models here.
@admin.register(GitHubRepo)
class GitHubRepoAdmin(admin.ModelAdmin):
    list_display = ('name','skip_scan')

@admin.register(GitHubTeam)
class GitHubTeamAdmin(admin.ModelAdmin):
    pass

@admin.register(GitHubTeamRepo)
class GitHubTeamRepoAdmin(admin.ModelAdmin):
    list_display = ('team','repository')

@admin.register(GitHubVulnerabilityCount)
class GitHubVulnerabilityCountAdmin(admin.ModelAdmin):
    list_display = ( 'repository','critical','high','moderate','low')

@admin.register(GitHubRepoVulnerabilites)
class GitHubRepoVulnerabilitesAdmin(admin.ModelAdmin):
    list_display = ( 'repository','identifier_type','identifier_value','severity_level','advisory_url')