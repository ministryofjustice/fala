#!/bin/bash
set -e

# Ensure .env exists
[ ! -f .env ] && cp .env.example .env

# Required versions
NODE_VERSION=20
PYTHON_VERSION=3.12

# ---- Node check ----
NODE_MAJOR=$(node -v 2>/dev/null | sed 's/v//' | cut -d. -f1)
[ -z "$NODE_MAJOR" ] || [ "$NODE_MAJOR" -lt "$NODE_VERSION" ] && {
  echo "Node >= $NODE_VERSION required"
  exit 1
}

# ---- Python check ----
PY_VERSION=$(python3 -V 2>/dev/null | awk '{print $2}')
PY_MAJOR=${PY_VERSION%%.*}
PY_MINOR=${PY_VERSION#*.}; PY_MINOR=${PY_MINOR%%.*}

REQ_MAJOR=${PYTHON_VERSION%%.*}
REQ_MINOR=${PYTHON_VERSION#*.}

[ "$PY_MAJOR" -lt "$REQ_MAJOR" ] || \
{ [ "$PY_MAJOR" -eq "$REQ_MAJOR" ] && [ "$PY_MINOR" -lt "$REQ_MINOR" ]; } && {
  echo "Python >= $PYTHON_VERSION required"
  exit 1
}

export ENVIRONMENT=${1:-development}
echo "running environment $ENVIRONMENT"

docker compose down --remove-orphans
docker compose up -d --build
docker compose exec webapp python3 manage.py migrate
docker compose logs -f webapp
