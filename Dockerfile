# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE=${DJANGO_SETTINGS_MODULE}
ENV TZ=Europe/Kiev

# Set work directory
WORKDIR /code

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install dependencies using Poetry
RUN pip install poetry
COPY pyproject.toml ./
RUN poetry config virtualenvs.create false \
    && poetry install --no-dev

# Copy project files into the docker image
COPY . .
COPY entrypoint-dev.sh /entrypoint-dev.sh
COPY entrypoint-prod.sh /entrypoint-prod.sh
