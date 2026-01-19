#!/bin/bash

# Ensure .env exists
[ ! -f .env ] && cp .env.example .env

# ---- Node check ----
NODE_MAJOR=$(node -v 2>/dev/null | cut -d. -f1 | tr -d v)
[ -z "$NODE_MAJOR" ] || [ "$NODE_MAJOR" -lt 20 ] && {
  echo "Node >= 20 required"
  exit 1
}

# ---- Python check ----
PY_VERSION=$(python3 -V 2>/dev/null | awk '{print $2}')
PY_MAJOR=$(echo "$PY_VERSION" | cut -d. -f1)
PY_MINOR=$(echo "$PY_VERSION" | cut -d. -f2)

[ "$PY_MAJOR" -lt 3 ] || { [ "$PY_MAJOR" -eq 3 ] && [ "$PY_MINOR" -lt 12 ]; } && {
  echo "Python >= 3.12 required"
  exit 1
}

export ENVIRONMENT=${1:-development}
echo "running environment $ENVIRONMENT"

docker compose down --remove-orphans
docker compose up -d --build
docker compose exec webapp python3 manage.py migrate
docker compose logs -f webapp
