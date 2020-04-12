FROM python:3.7-alpine
MAINTAINER Accalina

ENV PYTHONUNBUFFERED 1
WORKDIR /cloudwolf

COPY ./app .
RUN pip install -r requirements.txt
