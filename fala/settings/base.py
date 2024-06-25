# coding=utf-8
import sys
import os
from os.path import join, abspath, dirname

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration

# Load environment variables from .env file
from dotenv import load_dotenv

# With override set to True the value of the variable in `.env` is loaded first https://pypi.org/project/python-dotenv/#variable-expansion
load_dotenv(override=True)


def here(*x):
    return join(abspath(dirname(__file__)), *x)


PROJECT_ROOT = here("..")


def root(*x):
    return join(abspath(PROJECT_ROOT), *x)


sys.path.insert(0, root("apps"))

DEBUG = os.environ.get("DEBUG", False)
DEBUG = DEBUG == "True" or DEBUG is True

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("DB_NAME", "fala_development"),
        "USER": os.environ.get("DB_USER", ""),
        "PASSWORD": os.environ.get("DB_PASSWORD", "postgres"),
        "PORT": os.environ.get("DB_PORT", "5432"),
        "HOST": os.environ.get("DB_HOST", ""),
    }
}

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
                "adviser.context_processors.current_environment",
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
)

MIDDLEWARE = (
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "csp.middleware.CSPMiddleware",
)
CSP_DEFAULT_SRC = ["'self'", "*.googletagmanager.com"]
CSP_INCLUDE_NONCE_IN = ["script-src"]
CSP_SCRIPT_SRC = [
    "'self'",
    "*.googleapis.com",
    "*.gstatic.com",
    "*.google.com",
    "*.ggpht.com",
    "*.googleusercontent.com",
    "blob:",
    "ajax.aspnetcdn.com",
    "*.googletagmanager.com",
    "*.analytics.google.com",
    "*.g.doubleclick.net",
    "*.google.co.uk",
]
CSP_IMG_SRC = [
    "'self'",
    "*.googleapis.com",
    "*.gstatic.com",
    "*.google.com",
    "*.googleusercontent.com",
    "data:",
    "*.googletagmanager.com",
    "*.analytics.google.com",
    "*.google.co.uk",
    "*.g.doubleclick.net",
    "*.google-analytics.com",
]
CSP_FRAME_SRC = ["*.google.com"]
CSP_CONNECT_SRC = [
    "'self'",
    "*.googleapis.com",
    "*.google.com",
    "*.gstatic.com",
    "data:",
    "blob:",
    "*.google-analytics.com",
    "*.analytics.google.com",
    "*.googletagmanager.com",
    "*.g.doubleclick.net",
    "*.google.co.uk",
]
CSP_FONT_SRC = [
    "'self'",
    "data:",
    "fonts.gstatic.com",
]
CSP_STYLE_SRC = [
    "'self'",
    "'unsafe-inline'",
    "*.googleapis.com",
    "*.google.com",
    "*.google.co.uk",
    "fonts.googleapis.com",
    "*.gstatic.com",
]
CSP_WORKER_SRC = ["blob:"]

CSP_FORM_ACTION = ["'self'"]

CSP_FRAME_ANCESTORS = ["'self'"]

ROOT_URLCONF = "fala.urls"

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = "fala.wsgi.application"

INSTALLED_APPS = (
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "requests",
    "pytest_django",
)

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

# SENTRY CONFIG
if "SENTRY_DSN" in os.environ:
    sentry_sdk.init(
        dsn=os.environ.get("SENTRY_DSN"),
        integrations=[DjangoIntegration()],
        traces_sample_rate=1.0,
        environment=os.environ.get("ENVIRONMENT", "unknown"),
    )

LAALAA_API_HOST = os.environ.get("LAALAA_API_HOST", None)

FEATURE_FLAG_NO_MAP = os.environ.get("FEATURE_FLAG_NO_MAP", "").lower() == "true"

ENVIRONMENT = os.environ.get("ENVIRONMENT", "unknown")

GOOGLE_MAPS_API_KEY = os.environ.get("GOOGLE_MAPS_API_KEY", "")

CHECK_LEGAL_AID_URL = "https://www.gov.uk/check-legal-aid"

FEATURE_FLAG_SURVEY_MONKEY = os.environ.get("FEATURE_FLAG_SURVEY_MONKEY", "").lower() == "true"
