# -*- coding: utf-8 -*-
"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.0.4.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.0/ref/settings/
"""

import json
import os
import sys
from pathlib import Path

import dj_database_url
import environ
import sentry_sdk
from django_log_formatter_ecs import (
    ECSFormatter,
    ECSSystemFormatter,
    ECSRequestFormatter,
)
from sentry_sdk.integrations.django import DjangoIntegration

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = Path.joinpath(BASE_DIR, ".env")

env = environ.Env(DJANGO_DEBUG=(bool, False), DJANGO_RESTRICT_ADMIN=(bool, True))

if ENV_FILE.exists():
    environ.Env.read_env(str(ENV_FILE))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env("DJANGO_SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env("DJANGO_DEBUG", default=False)
DJANGO_DEBUG_LEVEL = env("DJANGO_DEBUG_LEVEL", default="INFO")
RESTRICT_ADMIN = env("DJANGO_RESTRICT_ADMIN", default=False)

ALLOWED_HOSTS = env.list("DJANGO_ALLLOWED_HOSTS", default=["127.0.0.1", "localhost"])

DEPLOYMENT_ENVIRONMENT = env("DEPLOYMENT_ENVIRONMENT", default="prod")

# GITHUB Variables
GITHUB_LOGIN = env("GITHUB_LOGIN")
GITHUB_AUTH_TOKEN = env("GITHUB_AUTH_TOKEN")
GITHUB_ORGANIZATION_NAME = env(
    "GITHUB_ORGANIZATION_NAME", default="Department for International Trade"
)
GITHUB_API_URL = env("GITHUB_API_URL", default="https://api.github.com/graphql")
GITHUB_FIRST_N_RECORDS = env.int("GITHUB_FIRST_N_RECORDS", default=100)
GITHUB_VERIFY_SSL = env.bool("GITHUB_VERIFY_SSL", default=True)
GITHUB_SKIP_SCAN_TOPIC = env(
    "GITHUB_SKIP_SCAN_TOPIC", default="skip-vulnerability-scan"
)
GITHUB_TEAMS_ARE_NOT_A_SSO_TARGET = env.list(
    "GITHUB_TEAMS_ARE_NOT_A_SSO_TARGET", default=[]
)
# SCANNER Variable
SCANNER_DATA_FILE_NAME = env("SCANNER_DATA_FILE_NAME", default=".scanner_data.json")
SCANNER_DATA_FILE_PATH = Path.joinpath(BASE_DIR, SCANNER_DATA_FILE_NAME)

# Report Variables
UK_HOLIDAYS_SOURCE_URL = env(
    "UK_HOLIDAYS_SOURCE_URL", default="https://www.gov.uk/bank-holidays.json"
)
UK_HOLIDAYS_FILE_NAME = env("UK_HOLIDAYS_FILE_NAME", default=".uk_bank_holidays.json")
UK_HOLIDAYS_FILE_PATH = Path.joinpath(BASE_DIR, UK_HOLIDAYS_FILE_NAME)

""" Maximum acceptable age of downloaded file defaults to 30 days"""
UK_HOLIDAYS_FILE_MAX_AGE = env("UK_HOLIDAYS_FILE_MAX_AGE", default=30)
PROCESSED_DATA_FILE_NAME = env(
    "PROCESSED_DATA_FILE_NAME", default=".processed_data.json"
)
PROCESSED_DATA_FILE_PATH = Path.joinpath(BASE_DIR, PROCESSED_DATA_FILE_NAME)

# mock test data which generates fake scanner_data with few possible combinations
if DEPLOYMENT_ENVIRONMENT != "prod":
    TEST_SCENES_FILE_NAME = env(
        "TEST_SCENES_FILE_NAME", default=".test_scenes_data.json"
    )
    TEST_SCENE_FILE_PATH = Path.joinpath(BASE_DIR, TEST_SCENES_FILE_NAME)

# Email config
ENABLE_GOV_NOTIFY = env.bool("ENABLE_GOV_NOTIFY", default=True)
GOV_NOTIFY_API_KEY = env("GOV_NOTIFY_API_KEY")
EMAIL_SIGNATURE = env("EMAIL_SIGNATURE")
GOV_NOTIFY_DETAILED_REPORT_TEMPLATE_ID = env("GOV_NOTIFY_DETAILED_REPORT_TEMPLATE_ID")
GOV_NOTIFY_SUMMARY_REPORT_TEMPLATE_ID = env("GOV_NOTIFY_SUMMARY_REPORT_TEMPLATE_ID")

if DEPLOYMENT_ENVIRONMENT != "prod":
    GOV_NOTIFY_FAKE_TEST_API_KEY = env("GOV_NOTIFY_FAKE_TEST_API_KEY")
    GOV_NOTIFY_REAL_TEST_API_KEY = env("GOV_NOTIFY_REAL_TEST_API_KEY")

# SLACK CONFIG
ENABLE_SLACK_NOTIFY = env.bool("ENABLE_SLACK_NOTIFY", default=True)
SLACK_MESSAGE_LENGTH = env.int("SLACK_MESSAGE_LENGTH", default=2800)
SLACK_URL = env("SLACK_URL")
SLACK_CHANNEL = env("SLACK_CHANNEL")
SLACK_AUTH_TOKEN = env("SLACK_AUTH_TOKEN")

# Gecko config
GECKO_BOARD_TOKEN = env("GECKO_BOARD_TOKEN")
GECKO_BOARD_TOP_N_REPOSITORIES = env.int("GECKO_BOARD_TOP_N_REPOSITORIES", default=20)

# SSO Config
ENABLE_SSO = env.bool("ENABLE_SSO", default=True)

ENABLE_REPORT_ENDPOINT = env.bool("ENABLE_REPORT_ENDPOINT", default=False)

# Enable Report WEB End Point
if ENABLE_REPORT_ENDPOINT:
    ALLOWED_REPORT_ENDPOINT_HOST = env(
        "ALLOWED_REPORT_ENDPOINT_HOST", default="localhost"
    )

SEVERITY_ESCLATION_MATRIC = {
    key: int(value)
    for key, value in env.dict(
        "SEVERITY_ESCLATION_MATRIC",
        default={"CRITICAL": 1, "HIGH": 7, "MODERATE": 15, "LOW": 255},
    ).items()
}


AUTHBROKER_URL = env("AUTHBROKER_URL", default="https://sso.trade.gov.uk")

if ENABLE_SSO:
    AUTHBROKER_CLIENT_ID = env("AUTHBROKER_CLIENT_ID")
    AUTHBROKER_CLIENT_SECRET = env("AUTHBROKER_CLIENT_SECRET")

AUTHENTICATION_BACKENDS = [
    "django.contrib.auth.backends.ModelBackend",
    "authbroker_client.backends.AuthbrokerBackend",
]


LOGIN_REDIRECT_URL = "admin:index"
AUTH_USER_MODEL = "user.User"

# LOGGING CONFIG
ECS_FORMATTERS = {
    "root": ECSSystemFormatter,
    "django.request": ECSRequestFormatter,
    "django.db.backends": ECSSystemFormatter,
}

LOGGING = {
    "version": 1.0,
    "disable_existing_loggers": False,
    "formatters": {
        "ecs_formatter": {
            "()": ECSFormatter,
        },
    },
    "handlers": {
        "ecs": {
            "formatter": "ecs_formatter",
            "class": "logging.StreamHandler",
            "stream": sys.stdout,
        },
    },
    "loggers": {
        "root": {  # or desired logger - "django" etc
            "handlers": ["ecs"],
            "level": f"{DJANGO_DEBUG_LEVEL}",
        },
    },
}

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "authbroker_client",
    "user",
    "common",
    "scanner",
    "report",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Initialise Sentry
sentry_sdk.init(
    dsn=env("SENTRY_DSN", default=None),
    integrations=[
        DjangoIntegration(
            transaction_style="url",
        ),
    ],
    release=env("GIT_COMMIT", default=None),
    environment=env("SENTRY_ENVIRONMENT", default=DEPLOYMENT_ENVIRONMENT),
)


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if "VCAP_SERVICES" in os.environ:
    services = json.loads(os.getenv("VCAP_SERVICES"))
    DATABASE_URL = services["postgres"][0]["credentials"]["uri"]
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

DATABASES = {"default": dj_database_url.config(engine="django.db.backends.postgresql")}


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

STATIC_URL = "static/"
STATIC_ROOT = Path.joinpath(BASE_DIR, STATIC_URL)

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
