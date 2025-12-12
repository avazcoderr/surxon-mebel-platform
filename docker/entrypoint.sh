#!/usr/bin/env bash
# Entrypoint script for Railway deployment

# Run migrations
python /app/surxon_backend/manage.py migrate --noinput

# Collect static files
python /app/surxon_backend/manage.py collectstatic --noinput

# Start the application
exec python /app/surxon_backend/manage.py runserver 0.0.0.0:$PORT