FROM node:10 as node_build

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

# Install Playwright dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
      libnss3 \
      libatk1.0-0 \
      libatk-bridge2.0-0 \
      libcups2 \
      libxcomposite1 \
      libxrandr2 \
      libxdamage1 \
      libxkbcommon0 \
      libpango-1.0-0 \
      libxshmfence1 \
      libgbm1

ENV HOME /home/app
ENV APP_HOME /home/app
WORKDIR /home/app

# Install Python dependencies
COPY ./requirements/generated/requirements-production.txt ./requirements.txt
RUN pip3 install --user --requirement ./requirements.txt

# Install Playwright and its browsers
RUN pip3 install playwright && playwright install --with-deps

COPY . .

RUN ./manage.py collectstatic --noinput

# Project permissions
RUN  chown -R app: /home/app

USER 1000
EXPOSE 8000
CMD ["/home/app/docker/run.sh"]
