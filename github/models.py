from django.db import models

# Create your models here.


class GitHubTeam(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)


class GitHubRepo(models.Model):
    id = models.CharField(primary_key=True, max_length=200)
    name = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.name)


class GitHubVulnerabilityAlters(models.Model):
    repository = models.CharField(primary_key=True, max_length=100)
    critical = models.IntegerField()
    high = models.IntegerField()
    moderate = models.IntegerField()
    low = models.IntegerField()

    def __str__(self):
        return '{}'.format(self.repository)


class GitHubTeamRepo(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.CharField(max_length=100)
    repository = models.CharField(max_length=100)

    def __str__(self):
        return '{}'.format(self.team)
