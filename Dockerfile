# Dockerfile for API Tool
# https://hub.docker.com/_/python/tags
ARG PYTHON_VERSION=3.12
ARG BUILD_VERSION=${PYTHON_VERSION}.1

###################################################
FROM python:${BUILD_VERSION}-alpine as builder

ENV TERM=xterm-256color \
    PYTHONFAULTHANDLER=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONHASHSEED=random \
    # PIP config
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # Default tool values
    DB_TYPE=sql \
    PROJECT_NAME=fastapi_nextjs_app

# Set working directory
WORKDIR /app

# Copy project and poetry files
COPY . /app/

# Install system dependencies
RUN apk update && \
    apk add --no-cache --virtual .build-deps build-base && \
    # Update and install poetry
    pip install --upgrade pip poetry && \
    poetry config virtualenvs.create false && \
    poetry install && \
    # Cleanup
    apk del .build-deps

# Run server
# CMD ["sleep", "infinity"]
CMD poetry run create $PROJECT_NAME $DB_TYPE
