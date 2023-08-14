#!/bin/bash

# Uncommnent this for prod
# Collect static files
echo "Collect static files"
python manage.py collectstatic --noinput --settings=core.settings.${SETTINGS_TYPE}

# # Apply database migrations
echo "Apply database migrations"
python manage.py migrate --settings=core.settings.${SETTINGS_TYPE}

# Start the server
exec "$@"
