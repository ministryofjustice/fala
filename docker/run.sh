#!/usr/bin/env bash
set -e

python manage.py migrate

# Run server
$HOME/.local/bin/uwsgi --ini $APP_HOME/conf/uwsgi.ini
