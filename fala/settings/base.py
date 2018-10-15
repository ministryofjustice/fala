# -*- coding: utf-8 -*-
import sys
import os
from os.path import join, abspath, dirname

import json

here = lambda *x: join(abspath(dirname(__file__)), *x)
PROJECT_ROOT = here("..")
root = lambda *x: join(abspath(PROJECT_ROOT), *x)

sys.path.insert(0, root('apps'))

DEBUG = os.environ.get('DEBUG', False)
DEBUG = DEBUG == 'True' or DEBUG is True
DEBUG_STATIC = False

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {}

ALLOWED_HOSTS = [
    '.laa-fala-staging.apps.cloud-platform-live-0.k8s.integration.dsd.io',
    '.fala.dsd.io',
    '.find-legal-advice.justice.gov.uk',
    'localhost'
]

LANGUAGE_CODE = 'en-gb'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_ROOT = root('assets', 'uploads')

MEDIA_URL = '/media/'

STATIC_ROOT = root('static')

STATIC_URL = '/static/'

project_root = abspath(root('..'))

# Additional locations of static files
STATICFILES_DIRS = (
    root('assets'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('SECRET_KEY', 'SET_THIS_IN_ENV')

TEMPLATES = [
    {
        'BACKEND': 'django_jinja.backend.Jinja2',
        'DIRS': [
            root('templates'),
            abspath(root(project_root, 'node_modules', 'mojular-templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'match_extension': '.html',
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                # 'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'adviser.context_processors.ga_id',
            ],
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # 'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
)

ROOT_URLCONF = 'fala.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'fala.wsgi.application'

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'requests',
)

PROJECT_APPS = (
    'adviser',
    'laalaa',
)

INSTALLED_APPS += PROJECT_APPS

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
        'logstash': {
            '()': 'logstash_formatter.LogstashFormatter'
        }
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        },
        'require_debug_true': {
            '()': 'django.utils.log.RequireDebugTrue'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        }
    }
}

LOGGING['handlers']['console'] = {
    'level': 'DEBUG',
    'class': 'logging.StreamHandler',
    'stream': sys.stdout
}

LOGGING['loggers'][''] = {
    'handlers': ['console'],
    'level': "DEBUG",
}

# RAVEN SENTRY CONFIG
if 'SENTRY_DSN' in os.environ:
    RAVEN_CONFIG = {
        'dsn': os.environ.get('SENTRY_DSN')
    }

    INSTALLED_APPS += (
        'raven.contrib.django.raven_compat',
    )

    MIDDLEWARE_CLASSES = (
        'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    ) + MIDDLEWARE_CLASSES

LAALAA_API_HOST = os.environ.get('LAALAA_API_HOST', 'http://0.0.0.0:8001')

# Zendesk settings for feedback
ZENDESK_API_USERNAME = os.environ.get('ZENDESK_API_USERNAME')
ZENDESK_API_TOKEN = os.environ.get('ZENDESK_API_TOKEN')
ZENDESK_GROUP_ID = os.environ.get('ZENDESK_GROUP_ID', 26974037) # Find a Legal Adviser (FALA)
ZENDESK_API_ENDPOINT = 'https://ministryofjustice.zendesk.com/api/v2/'
ZENDESK_REQUESTER_ID = os.environ.get('ZENDESK_REQUESTER_ID', 649762516)
# defaults to 'anonymous feedback <noreply@ministryofjustice.zendesk.com>'

GA_ID = os.environ.get('GA_ID')

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass
