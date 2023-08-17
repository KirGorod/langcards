#!/bin/bash

# Uncommnent this for prod
# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput --settings=${DJANGO_SETTINGS_MODULE}

# # Apply database migrations
echo "Apply database migrations"
python manage.py migrate --settings=${DJANGO_SETTINGS_MODULE}

# Start the server
exec "$@"
