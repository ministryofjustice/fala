#!/bin/bash
if [ ! -f fala/settings/local.py ]; then
  cp fala/settings/local.example.py fala/settings/local.py
fi

docker-compose up --build
