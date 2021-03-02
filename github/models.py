from django.db import models

# Create your models here.
class GitHubRepo(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    skip_scan = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.name)

class GitHubTeam(models.Model):
    name = models.CharField(primary_key=True, max_length=100)

    def __str__(self):
        return '{}'.format(self.name)

class GitHubTeamRepo(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey('GitHubTeam',on_delete=models.CASCADE)
    repository = models.ForeignKey('GitHubRepo',on_delete=models.CASCADE)

class GitHubRepoVulnerabilites(models.Model):
    id = models.AutoField(primary_key=True)
    repository = models.ForeignKey('GitHubRepo',on_delete=models.CASCADE)
    package_name = models.CharField(max_length=50)
    severity_level = models.CharField(max_length=20)
    identifier_type = models.CharField(max_length=20)
    identifier_value = models.CharField(max_length=20)
    advisory_url = models.CharField(max_length=200,null=True)

class GitHubVulnerabilityCount(models.Model):
    repository = models.ForeignKey('GitHubRepo',on_delete=models.CASCADE)
    critical = models.IntegerField()
    high = models.IntegerField()
    moderate = models.IntegerField()
    low = models.IntegerField()