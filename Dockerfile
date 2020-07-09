FROM python:3.8
USER root

COPY ./requirements.txt /requirements.txt

RUN apt-get update

RUN pip install --upgrade pip
RUN pip install -r /requirements.txt