#!/usr/bin/env bash
set -e

# Run server
$HOME/.local/bin/uwsgi --ini $APP_HOME/conf/uwsgi.ini
