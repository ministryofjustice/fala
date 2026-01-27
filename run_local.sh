
#!/bin/bash
if [ ! -f .env ]; then
  cp .env.example .env
fi

export ENVIRONMENT=${1:-development}
echo "running environment $ENVIRONMENT"
docker compose down --remove-orphans

docker compose up -d --build
docker compose exec webapp python3 manage.py migrate
docker compose exec webapp python3 manage.py collectstatic --noinput
docker compose logs -f webapp
