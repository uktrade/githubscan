# -*- coding: utf-8 -*-
import os
from ssl import CERT_NONE

from celery import Celery

from config import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

app = Celery("config")

app.config_from_object("django.conf:settings", namespace="CELERY")

ssl_conf = {
    "ssl_cert_reqs": CERT_NONE,
    "ssl_ca_certs": None,
    "ssl_certfile": None,
    "ssl_keyfile": None,
}

app.conf.CELERY_BROKER_URL = settings.CELERY_BROKER_URL

if "VCAP_SERVICES" in os.environ:
    app.conf.broker_use_ssl = ssl_conf
    app.conf.redis_backend_use_ssl = ssl_conf
else:
    app.conf.broker_use_ssl = False
    app.conf.redis_backend_use_ssl = False

app.conf.broker_connection_retry_on_startup = True

app.autodiscover_tasks()
