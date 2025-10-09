#!/bin/bash -e

cd /home/app

# Run migrations
./manage.py migrate --noinput

echo "Database setup and Django migrations completed successfully."

exec "$@"


