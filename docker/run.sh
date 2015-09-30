#!/usr/bin/env bash
set -e

# Run server
/usr/local/bin/uwsgi --ini /home/app/conf/uwsgi.ini
