#!/bin/bash
if [ ! -f .env ]; then
  cp .env.example .env
fi

docker-compose up -d --build
docker-compose run webapp python3 manage.py collectstatic --no-input
docker-compose logs -f webapp


