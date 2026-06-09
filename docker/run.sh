#!/usr/bin/env bash
set -e

# Run server
$HOME/.local/bin/gunicorn --config $APP_HOME/conf/gunicorn.conf.py
