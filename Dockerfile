FROM python:3.7-alpine
MAINTAINER HousewifeHacker

# recommended for Python with Docker
ENV PYTHONUNBUFFERED 1

# Install dependencies
# create and then delete directory
COPY ./requirements.txt /requirements.txt
RUN apk add --update --no-cache postgresql-client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
      gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt
RUN apk del .tmp-build-deps

# Setup directory structure, copy from local to new container directory
RUN mkdir /app
WORKDIR /app
COPY ./app/ /app

# use a non ROOT user with default values
RUN adduser -D user
USER user