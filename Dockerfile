FROM  python:3.10.1-slim-buster

RUN apt-get update
RUN apt-get -y install libpq-dev gcc
RUN pip3 install --upgrade pip
RUN pip3 install pipenv