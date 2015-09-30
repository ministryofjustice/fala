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

ADMINS = ()

MANAGERS = ADMINS

DATABASES = {}

ALLOWED_HOSTS = [
    '.dsd.io',
]

TIME_ZONE = 'Europe/London'

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

bower_dir = json.load(open(join(project_root, '.bowerrc')))['directory']

# Additional locations of static files
STATICFILES_DIRS = (
    root('assets'),
    abspath(root(project_root, bower_dir, 'govuk-template', 'assets')),
    abspath(root(project_root, bower_dir, 'mojular', 'assets'))
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ.get('SECRET_KEY', None)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            root('templates'),
            abspath(root(project_root, bower_dir, 'mojular', 'templates')),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
            'debug': DEBUG,
        },
    },
]

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
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

    'raven.contrib.django.raven_compat',
    'requests',
)

PROJECT_APPS = (
    'adviser',
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
    },
    'handlers': {
        'console': {
            'level': 'WARN',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
            'propagate': True,
            'level': 'WARN',
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        }
    }
}

RAVEN_CONFIG = {
    'dsn': os.environ.get('SENTRY_DSN'),
}

# .local.py overrides all the common settings.
try:
    from .local import *
except ImportError:
    pass
