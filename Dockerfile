FROM docker.io/node:25.9.0-trixie@sha256:74ff139f927c4a233bf0757edefe1ee057d185d6548c65d2741bdda68660fb6a AS node_build

WORKDIR /home/node

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN ./node_modules/.bin/gulp build --production

#################################################
# BASE IMAGE USED BY ALL STAGES
#################################################
FROM python:3.15-rc-alpine AS base

ENV LC_CTYPE=C.UTF-8

# Create runtime user early, then use that user in child stages.
RUN addgroup -g 1000 app && adduser -u 1000 -G app -D -h /home/app app

# Install OS dependencies required by Python builds and runtime scripts.
RUN apk add --no-cache \
  bash \
  build-base \
  gettext \
  pcre2-dev

ENV HOME=/home/app \
  APP_HOME=/home/app \
  PATH=/home/app/.local/bin:$PATH
WORKDIR /home/app

COPY --from=node_build --chown=app:app home/node/fala/assets /home/app/fala/assets

USER app

#################################################
# DEVELOPMENT
#################################################

FROM base AS development

# Install Python dependencies for development, includes tests.
COPY --chown=app:app ./requirements/generated/requirements-dev.txt ./requirements.txt
RUN pip3 install --user --requirement ./requirements.txt

RUN playwright install

COPY --chown=app:app fala/ fala/
COPY --chown=app:app manage.py manage.py

RUN ./manage.py collectstatic --noinput
EXPOSE 8000
CMD ["/home/app/docker/run.sh"]

#################################################
# PRODUCTION
#################################################
FROM base AS production

# Install Python dependencies
COPY --chown=app:app ./requirements/generated/requirements-production.txt ./requirements.txt
RUN pip3 install --user --requirement ./requirements.txt

# Copy migrate_db.sh to the /home/app/fala directory
COPY --chown=app:app fala/migrate_db.sh /home/app/fala/migrate_db.sh
RUN chmod +x /home/app/fala/migrate_db.sh

COPY --chown=app:app . .

# Compile translation files
RUN python manage.py compilemessages -l cy

RUN ./manage.py collectstatic --noinput
EXPOSE 8000
CMD ["/home/app/docker/run.sh"]
