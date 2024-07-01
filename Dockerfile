FROM node:18-alpine as node_build

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN NODE_ENV=production npm run build

FROM python:3.12-bullseye

COPY --from=node_build ./fala/assets /home/app/fala/assets
# we are serving govuk-frontend images and fonts directly via the /assets url, so we have to copy them
# here into the same location that they were built into.
COPY --from=node_build ./node_modules/govuk-frontend/dist/govuk/assets /home/app/fala/node_modules/govuk-frontend/dist/govuk/assets
COPY --from=node_build ./fala/webpack-stats.json /home/app/fala

ENV LC_CTYPE=C.UTF-8

# Runtime User
RUN useradd --uid 1000 --user-group -m -d /home/app app

# Install python and build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      curl \
      git \
      libpcre3 \
      libpcre3-dev

ENV HOME /home/app
ENV APP_HOME /home/app
WORKDIR /home/app

# Install Python dependencies
COPY ./requirements/generated/requirements-production.txt ./requirements.txt
RUN pip3 install --user --requirement ./requirements.txt

# Copy migrate_db.sh to the /home/app/fala directory
COPY fala/migrate_db.sh /home/app/fala/migrate_db.sh

# Ensure the correct ownership
RUN chown app:app /home/app/fala/migrate_db.sh

# Ensure the script has execute permissions
RUN chmod +x /home/app/fala/migrate_db.sh

COPY . .

RUN ./manage.py collectstatic --noinput

# Project permissions
RUN  chown -R app: /home/app

USER 1000
EXPOSE 8000
CMD ["/home/app/docker/run.sh"]
