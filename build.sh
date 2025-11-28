#!/usr/bin/env bash
# build.sh

# Exit on error
set -o errexit

pip install --upgrade pip
pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py migrate