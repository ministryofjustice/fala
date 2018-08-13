FROM ubuntu:trusty-20180712

LABEL summary="Find A Legal Adviser" \
      name="fala" \
      version="1.0" \
      maintainer="Legal Aid Agency, Get Access <laa-get-access@digital.justice.gov.uk>"

RUN locale-gen "en_US.UTF-8"
ENV LC_CTYPE=en_US.UTF-8

# Install Node.js, npm, gulp
RUN apt-get update && \
    apt-get install -y \
      build-essential \
      curl \
      git \
      python-minimal && \
    curl -sL https://deb.nodesource.com/setup_8.x | sudo -E bash && \
    apt-get install -y nodejs && \
    apt-get clean && \
    npm install --global npm@5.6.0 && \
    npm install --global gulp

# Install Python3
RUN apt-get update && \
    apt-get install -y \
      libpcre3 libpcre3-dev \
      python3-all python3-all-dev \
      python3-pip \
      && \
    apt-get clean && \
    update-alternatives --install /usr/bin/python python /usr/bin/python3 10

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

RUN gulp --production && \
    ./manage.py collectstatic --noinput

EXPOSE 8000
CMD ["/home/app/docker/run.sh"]
