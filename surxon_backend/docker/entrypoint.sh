#!/usr/bin/env bash
# Entrypoint script for Railway deployment

# Collect static files
python manage.py collectstatic --noinput

# Run migrations
python manage.py migrate --noinput

# Start the application
exec python manage.py runserver 0.0.0.0:$PORT