#!/usr/bin/env bash
set -e

python manage.py rewrite_paths_in_static_files
python manage.py collectstatic --noinput
