# -*- coding: utf-8 -*-
from django.contrib import admin

from common.models import JsonStore


@admin.register(JsonStore)
class JsonStoreAdmin(admin.ModelAdmin):
    """Json Store Admin Interface"""

    list_display = ("scanned_data", "processed_data")
