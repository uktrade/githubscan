# -*- coding: utf-8 -*-
from .views import refresh_vulneranility_data
from django.urls import path, include

urlpatterns = [
    path(
        "refresh_vulneranility_data/",
        refresh_vulneranility_data,
        name="refresh_vulneranility_data",
    )
]
