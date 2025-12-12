#!/usr/bin/env bash
# Railway deployment script

cd ..

# Run migrations
python manage.py migrate --noinput

# Collect static files
python manage.py collectstatic --noinput

# Start the server
python manage.py runserver 0.0.0.0:$PORT