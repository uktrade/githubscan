from django.db import models
from django.utils import timezone
# Create your models here.


class Repository(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    skip_scan = models.BooleanField(default=False)

    def __str__(self):
        return '{}'.format(self.name)


class Team(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    repositories = models.ManyToManyField(Repository)

    def __str__(self):
        return '{}'.format(self.name)


class RepositoryVulnerability(models.Model):
    id = models.AutoField(primary_key=True)
    repository = models.ForeignKey('Repository', on_delete=models.CASCADE)
    package_name = models.CharField(max_length=50)
    severity_level = models.CharField(max_length=20)
    identifier_type = models.CharField(max_length=20)
    identifier_value = models.CharField(max_length=20)
    advisory_url = models.CharField(max_length=200, null=True)
    published_at = models.DateTimeField(default=timezone.now)
    detection_date = models.DateTimeField(auto_now_add=True)
    publish_age_in_days = models.IntegerField(default=0)
    detection_age_in_days = models.IntegerField(default=0)
    slo_breach = models.BooleanField(default=False)


class RepositoryVulnerabilityCount(models.Model):
    repository = models.ForeignKey('Repository', on_delete=models.CASCADE)
    critical = models.IntegerField()
    high = models.IntegerField()
    moderate = models.IntegerField()
    low = models.IntegerField()

class RepositorySLOBreachCount(models.Model):
    repository = models.ForeignKey('Repository', on_delete=models.CASCADE)
    critical = models.IntegerField()
    high = models.IntegerField()
    moderate = models.IntegerField()
    low = models.IntegerField()
