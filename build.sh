#!/usr/bin/env bash
# Exit on errors
set -o errexit

# 1. Install dependencies
pip install -r requirements.txt

# 2. Run database migrations
python manage.py migrate

# 3. Create admin user if none exists (using environment variables)
python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser(
        os.environ.get('ADMIN_USER', 'admin'),
        os.environ.get('ADMIN_EMAIL', 'admin@shop.com'),
        os.environ.get('ADMIN_PASSWORD')
    )
EOF

# 4. Collect static files
python manage.py collectstatic --noinput