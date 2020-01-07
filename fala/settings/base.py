# coding=utf-8
import sys
import os
from os.path import join, abspath, dirname


def here(*x):
    return join(abspath(dirname(__file__)), *x)


PROJECT_ROOT = here("..")


def root(*x):
    return join(abspath(PROJECT_ROOT), *x)


sys.path.insert(0, root("apps"))

DEBUG = os.environ.get("DEBUG", False)
DEBUG = DEBUG == "True" or DEBUG is True
DEBUG_STATIC = os.environ.get("DEBUG_STATIC", False)

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {}

DEFAULT_ALLOWED_HOSTS = ".fala.dsd.io .find-legal-advice.justice.gov.uk"
ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS", DEFAULT_ALLOWED_HOSTS).split(" ")

LANGUAGE_CODE = "en-gb"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = root("assets", "uploads")

MEDIA_URL = "/media/"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/
if os.environ.get("STATIC_FILES_BACKEND") == "s3":
    STATICFILES_STORAGE = "storages.backends.s3boto3.S3Boto3Storage"

AWS_STORAGE_BUCKET_NAME = os.environ.get("AWS_STORAGE_BUCKET_NAME")
AWS_ACCESS_KEY_ID = os.environ.get("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.environ.get("AWS_SECRET_ACCESS_KEY")
AWS_S3_REGION_NAME = os.environ.get("AWS_S3_REGION_NAME")
AWS_DEFAULT_ACL = None
AWS_QUERYSTRING_EXPIRE = 60 * 60 * 24 * 7

STATIC_URL = "/static/"
STATIC_ROOT = root("static")

project_root = abspath(root(".."))

# Additional locations of static files
STATICFILES_DIRS = (root("assets"),)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder",
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get("SECRET_KEY", "SET_THIS_IN_ENV")

TEMPLATES = [
    {
        "BACKEND": "django_jinja.backend.Jinja2",
        "DIRS": [root("templates"), abspath(root(project_root, "node_modules", "mojular-templates"))],
        "APP_DIRS": True,
        "OPTIONS": {
            "match_extension": ".html",
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                # 'django.contrib.auth.context_processors.auth',
                "django.contrib.messages.context_processors.messages",
                "adviser.context_processors.ga_id",
            ],
        },
    }
]

MIDDLEWARE_CLASSES = (
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
)

ROOT_URLCONF = "fala.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "fala.wsgi.application"

INSTALLED_APPS = ("django.contrib.sessions", "django.contrib.messages", "django.contrib.staticfiles", "requests")

PROJECT_APPS = ("adviser", "fala", "laalaa")

INSTALLED_APPS += PROJECT_APPS

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "verbose": {"format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s"},
        "simple": {"format": "%(levelname)s %(message)s"},
        "logstash": {"()": "logstash_formatter.LogstashFormatter"},
    },
    "handlers": {
        "console": {"level": "DEBUG", "class": "logging.StreamHandler", "stream": sys.stdout, "formatter": "logstash"}
    },
    "loggers": {"root": {"level": "DEBUG", "handlers": ["console"]}},
}

# RAVEN SENTRY CONFIG
if "SENTRY_DSN" in os.environ:
    RAVEN_CONFIG = {"dsn": os.environ.get("SENTRY_DSN")}

    INSTALLED_APPS += ("raven.contrib.django.raven_compat",)

    MIDDLEWARE_CLASSES = (
        "raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware",
    ) + MIDDLEWARE_CLASSES

LAALAA_API_HOST = os.environ.get("LAALAA_API_HOST", None)

# Zendesk settings for feedback
ZENDESK_API_USERNAME = os.environ.get("ZENDESK_API_USERNAME")
ZENDESK_API_TOKEN = os.environ.get("ZENDESK_API_TOKEN")
ZENDESK_GROUP_ID = os.environ.get("ZENDESK_GROUP_ID", 26974037)  # Find a Legal Adviser (FALA)
ZENDESK_API_ENDPOINT = "https://ministryofjustice.zendesk.com/api/v2/"
ZENDESK_REQUESTER_ID = os.environ.get("ZENDESK_REQUESTER_ID", 649762516)
# defaults to 'anonymous feedback <noreply@ministryofjustice.zendesk.com>'

GA_ID = os.environ.get("GA_ID")

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

# .local.py overrides all the common settings.
try:
    from .local import *  # noqa: F401,F403
except ImportError:
    pass
