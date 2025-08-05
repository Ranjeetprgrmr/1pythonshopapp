#!/usr/bin/env bash
set -o errexit

# Install system dependencies
sudo apt-get update
sudo apt-get install -y libpq-dev python3-dev

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt

# Apply database migrations
python manage.py migrate

# Collect static files
python manage.py collectstatic --noinput