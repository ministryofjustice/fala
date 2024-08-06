#!/bin/bash
if [ ! -f .env ]; then
  cp .env.example .env
fi

export ENVIRONMENT=${1:-development}
echo "running environment $ENVIRONMENT"
docker-compose down --remove-orphans

docker-compose up -d --build
# This has to be run outside of the container, because the
# entire(?) application is replaced with the local fala directory
# when run via docker-compose
NODE_ENV=production npm run build
python manage.py collectstatic --noinput
docker-compose exec webapp python3 manage.py migrate
docker-compose logs -f webapp


