FROM node:14 as node_build

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN ./node_modules/.bin/gulp build --production

#################################################
# BASE IMAGE USED BY ALL STAGES
#################################################
FROM python:3.12-bullseye as base

COPY --from=node_build ./fala/assets /home/app/fala/assets

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

#################################################
# DEVELOPMENT
#################################################

FROM base AS development

# Install Python dependencies for development, includes tests.
COPY ./requirements/generated/requirements-dev.txt ./requirements.txt
RUN pip3 install --user --requirement ./requirements.txt

# Add .local/bin to PATH to allow playwright command execution
ENV PATH=/home/app/.local/bin:$PATH
RUN playwright install --with-deps

COPY fala/ fala/
COPY manage.py manage.py

RUN ./manage.py collectstatic --noinput

# Project permissions
RUN  chown -R app: /home/app

USER 1000
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
