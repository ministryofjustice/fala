FROM node:10 as node_build

COPY package.json package-lock.json ./
# On the Git protocol side, unencrypted git:// offers no integrity or authentication, making it subject to tampering.
# We expect very few people are still using this protocol, especially given that you can’t push (it’s read-only on GitHub).
# We’ll be disabling support for this protocol.
# https://github.blog/2021-09-01-improving-git-protocol-security-github/#no-more-unauthenticated-git
RUN git config --global url."https://".insteadOf git://
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
