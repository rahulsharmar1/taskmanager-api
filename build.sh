#!/usr/bin/env bash
# build.sh — executed by Render during each deployment

set -o errexit  # exit immediately if any command fails

# Install all Python dependencies
pip install -r requirements.txt

# Collect static files into STATIC_ROOT (served by WhiteNoise)
python manage.py collectstatic --no-input

# Run any pending database migrations
python manage.py migrate

# Create superuser without interaction
python manage.py createsuperuser --no-input || true