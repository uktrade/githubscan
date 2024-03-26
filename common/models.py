# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.deletion import CASCADE


class JsonStore(models.Model):
    """
    Class to store json string

    This is a temporary fix, ideally we should put some time in to move data to data base now that,
    both size of active repositories and, complexity of project has grown
    """

    scanned_data = models.TextField(blank=True)
    scanned_data_time = models.DateTimeField(blank=True, null=True)
    processed_data = models.TextField(blank=True)
    processed_data_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        app_label = "common"
