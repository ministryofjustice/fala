FROM ubuntu:trusty-20180712

LABEL summary="Find A Legal Adviser" \
      name="fala" \
      version="1.0" \
      maintainer="Legal Aid Agency, Get Access <laa-get-access@digital.justice.gov.uk>"

RUN locale-gen "en_US.UTF-8"
ENV LC_CTYPE=en_US.UTF-8

# Install python and build dependencies
RUN apt-get update && \
    apt-get -y --force-yes install \
        build-essential \
        curl \
        git \
        libpcre3 \
        libpcre3-dev \
        python-minimal \
        python3-all \
        python3-all-dev \
        python3-pip && \
        update-alternatives --install /usr/bin/python python /usr/bin/python3 10

# Install NodeJS
RUN curl -sL https://deb.nodesource.com/setup_8.x | bash - && \
    apt-get -y --force-yes install nodejs

ENV HOME /home/app
ENV APP_HOME /home/app
WORKDIR /home/app

# Install Python dependencies
COPY ./requirements/base.txt ./requirements.txt
RUN pip3 install --user --requirement ./requirements.txt

# Install npm dependencies
COPY package.json package-lock.json ./
RUN npm install

COPY . .

RUN ./node_modules/.bin/gulp build --production && \
    ./manage.py collectstatic --noinput

EXPOSE 8000
CMD ["/home/app/docker/run.sh"]
