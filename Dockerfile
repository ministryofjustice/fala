#
# FALA Dockerfile all environments
#
FROM ubuntu:trusty-20150814

MAINTAINER Josh Rowe <josh.rowe@digital.justice.gov.uk>

# Runtime User
RUN useradd -m -d /home/app app

RUN locale-gen "en_US.UTF-8"
ENV LC_CTYPE=en_US.UTF-8

RUN apt-get update && \
    apt-get install -y software-properties-common python-software-properties

RUN add-apt-repository -y ppa:chris-lea/node.js

RUN apt-get update && \
    apt-get install -y \
        build-essential git python3-all python3-all-dev python3-setuptools \
        curl libpq-dev ntp ruby ruby-dev nodejs python3-pip python-pip

RUN update-alternatives --install /usr/bin/python python /usr/bin/python3 10

RUN npm install -g gulp

# Add requirements to docker
ADD ./requirements/base.txt /requirements.txt
RUN pip3 install -r /requirements.txt

# Add project directory to docker
ADD . /home/app
RUN rm -rf /home/app/.git
RUN  chown -R app: /home/app

RUN cd /home/app && npm install --unsafe-perm && gulp

RUN cd /home/app && ./manage.py collectstatic --noinput

# Set correct environment variables.
ENV HOME /home/app
WORKDIR /home/app
ENV APP_HOME /home/app
USER app
EXPOSE 8000
ENTRYPOINT ["/home/app/docker/run.sh"]
