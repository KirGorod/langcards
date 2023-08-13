# Use an official Python runtime as a parent image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

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
