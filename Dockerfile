FROM python:3.7-alpine
MAINTAINER HousewifeHacker

# recommended for Python with Docker
ENV PYTHONUNBUFFERED 1

# Install dependencies
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Setup directory structure, copy from local to new container directory
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

# use a non ROOT user with default values
RUN adduser -D user
USER user