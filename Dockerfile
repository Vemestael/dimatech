FROM python:3.11.0b4-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /var/www/html

RUN apt-get update \
    && apt-get install -y python3-dev libpq-dev gcc

COPY ./src/requirements.txt /var/www/html
RUN pip3 install -r requirements.txt

ADD ./src /var/www/html