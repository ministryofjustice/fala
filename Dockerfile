FROM node:12 as node_build

COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN ./node_modules/.bin/gulp build --production

FROM python:3.12-bullseye

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

# Install Python dependencies
COPY ./requirements/generated/requirements-production.txt ./requirements.txt
RUN pip3 install --user --requirement ./requirements.txt

COPY . .

RUN ./manage.py collectstatic --noinput

# Project permissions
RUN  chown -R app: /home/app

USER 1000
EXPOSE 8000
CMD ["/home/app/docker/run.sh"]
