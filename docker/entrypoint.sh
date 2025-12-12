#!/usr/bin/env bash
# Entrypoint script for Railway deployment

# Change to backend directory
cd /app/surxon_backend

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the application
exec python manage.py runserver 0.0.0.0:$PORT