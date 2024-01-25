#!/bin/bash
if [ ! -f fala/settings/local.py ]; then
  cp fala/settings/local.example.py fala/settings/local.py
fi

docker-compose up -d --build
docker-compose run webapp python3 manage.py collectstatic --no-input
docker-compose logs -f webapp
