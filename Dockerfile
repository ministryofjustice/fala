FROM docker.io/node:25.9.0-trixie@sha256:74ff139f927c4a233bf0757edefe1ee057d185d6548c65d2741bdda68660fb6a AS node_build

WORKDIR /home/node

COPY package.json package-lock.json ./
RUN npm ci

COPY gulpfile.js ./
COPY fala/assets-src/ fala/assets-src/

RUN ./node_modules/.bin/gulp build --production

#################################################
# BASE IMAGE USED BY ALL STAGES
#################################################
FROM python:3.15-rc-alpine@sha256:c8a2b555f655e34e8616f94fbc08e4e54cc381a4a8437cce3e5736fd818f790c AS base

ENV LC_CTYPE=C.UTF-8

# Create runtime user early, then use that user in child stages.
RUN addgroup -g 1000 app && adduser -u 1000 -G app -D -h /home/app app \
  && apk add --no-cache \
    bash=5.3.9-r1 \
    build-base=0.5-r4 \
    gettext=1.0-r0 \
    pcre2-dev=10.47-r1

ENV HOME=/home/app \
  APP_HOME=/home/app \
  TMPDIR=/home/app/tmp \
  PIP_NO_CACHE_DIR=1 \
  PATH=/home/app/.local/bin:$PATH
WORKDIR /home/app

COPY --from=node_build --chown=root:root home/node/fala/assets /home/app/fala/assets

RUN mkdir -p /home/app/tmp && chown app:app /home/app/tmp

USER app

#################################################
# DEVELOPMENT
#################################################

FROM base AS development

# Install Python dependencies for development, includes tests.
COPY ./requirements/generated/requirements-dev.txt ./requirements.txt
RUN pip3 install --user --requirement ./requirements.txt \
  && playwright install

COPY fala/ fala/
COPY manage.py manage.py

USER root
RUN chown -R app:app /home/app/fala/static
USER app
RUN ./manage.py collectstatic --noinput
EXPOSE 8000
CMD ["/home/app/docker/run.sh"]

#################################################
# PRODUCTION
#################################################
FROM base AS production

# Install Python dependencies
COPY ./requirements/generated/requirements-production.txt ./requirements.txt
RUN pip3 install --user --requirement ./requirements.txt

# Copy migrate_db.sh to the /home/app/fala directory
COPY --chmod=755 fala/migrate_db.sh /home/app/fala/migrate_db.sh

COPY conf/ conf/
COPY docker/ docker/
COPY fala/ fala/
COPY manage.py manage.py

# Compile translation files
USER root
RUN mkdir -p /home/app/fala/static \
  && chown -R app:app /home/app/fala/locale /home/app/fala/static
USER app
RUN python manage.py compilemessages -l cy \
  && ./manage.py collectstatic --noinput

# Harden copied resources: make them root-owned and non-writable by group/others
USER root
RUN chown -R root:root /home/app \
  && chmod -R go-w /home/app
USER app
EXPOSE 8000
CMD ["/home/app/docker/run.sh"]
