#!/bin/bash
if [ ! -f fala/settings/.env ]; then
  cp fala/settings/.env.example fala/settings/.env
fi

docker-compose up -d --build
docker-compose run webapp python3 manage.py collectstatic --no-input
docker-compose logs -f webapp
