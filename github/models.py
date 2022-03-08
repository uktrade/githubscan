from django.db import models
from django.db.models.deletion import CASCADE
from django.utils import timezone

# Create your models here.


class Repository(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    skip_scan = models.BooleanField(default=False)

    def __str__(self):
        return "{}".format(self.name)


class Team(models.Model):
    name = models.CharField(primary_key=True, max_length=100)
    repositories = models.ManyToManyField(Repository)
    reporting_enabled = models.BooleanField(
        default=True,
        help_text="Set True (checked / on) to enable reporting for this team.",
    )

    def __str__(self):
        return "{}".format(self.name)


class OrganisationNotificationTarget(models.Model):
    """Notification target details for the application instance's owning
    organisation (held by the settings attribute ORG_NAME which is set from
    and env var of the same name).
    """

    email = models.EmailField(
        unique=True,
        help_text="Target email address for organisation-level notifications.",
    )

    def __str__(self):
        return self.email


class TeamNotificationTarget(models.Model):
    team = models.ForeignKey(
        "Team",
        on_delete=CASCADE,
    )
    email = models.EmailField(
        help_text="Target email address for team-level notifications.",
    )
    red_alerts_only = models.BooleanField(
        default=False,
        help_text=(
            "Set True (checked/on) to prevent green status notifications being " "sent."
        ),
    )

    class Meta:
        unique_together = ("team", "email")

    def __str__(self):
        return f"{self.team}:{self.email}"


class RepositoryVulnerability(models.Model):
    id = models.AutoField(primary_key=True)
    repository = models.ForeignKey("Repository", on_delete=models.CASCADE)
    package_name = models.CharField(max_length=50)
    severity_level = models.CharField(max_length=20)
    effective_severity_level = models.CharField(max_length=20, blank=True)
    identifier_type = models.CharField(max_length=20)
    identifier_value = models.CharField(max_length=20)
    advisory_url = models.CharField(max_length=200, null=True)
    published_at = models.DateTimeField(default=timezone.now)
    detection_date = models.DateTimeField(default=timezone.now)
    publish_age_in_days = models.IntegerField(default=0)
    detection_age_in_days = models.IntegerField(default=0)
    time_since_current_level = models.IntegerField(default=0)
    slo_breach = models.BooleanField(default=False)
    patched_version = models.CharField(max_length=20, blank=True)


class RepositoryVulnerabilityCount(models.Model):
    id = models.AutoField(primary_key=True)
    repository = models.ForeignKey("Repository", on_delete=models.CASCADE)
    critical = models.IntegerField()
    high = models.IntegerField()
    moderate = models.IntegerField()
    low = models.IntegerField()
    effective_slabreach = models.IntegerField(default=0)
    effective_critical = models.IntegerField(default=0)
    effective_high = models.IntegerField(default=0)
    effective_moderate = models.IntegerField(default=0)
    effective_low = models.IntegerField(default=0)


class RepositorySLOBreachCount(models.Model):
    id = models.AutoField(primary_key=True)
    repository = models.ForeignKey("Repository", on_delete=models.CASCADE)
    critical = models.IntegerField()
    high = models.IntegerField()
    moderate = models.IntegerField()
    low = models.IntegerField()


class TeamVulnerabilityCount(models.Model):
    id = models.AutoField(primary_key=True)
    team = models.ForeignKey("Team", on_delete=models.CASCADE)
    critical = models.IntegerField()
    high = models.IntegerField()
    moderate = models.IntegerField()
    low = models.IntegerField()
    effective_slabreach = models.IntegerField(default=0)
    effective_critical = models.IntegerField(default=0)
    effective_high = models.IntegerField(default=0)
    effective_moderate = models.IntegerField(default=0)
    effective_low = models.IntegerField(default=0)
