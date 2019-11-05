#!/usr/bin/env bash
set -e

python manage.py rewrite_paths_in_css
python manage.py collectstatic
