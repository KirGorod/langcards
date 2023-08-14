#!/bin/sh

# Run collectstatic command
python manage.py collectstatic --noinput

# Start the Django development server
python manage.py runserver 0.0.0.0:8000
