#!/usr/bin/env bash
set -e

python manage.py collectstatic --noinput
