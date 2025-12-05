from django.apps import AppConfig
import os


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.contrib.auth import get_user_model
        from django.db.utils import OperationalError, ProgrammingError

        username = os.environ.get('RENDER_SUPERUSER_USERNAME')
        email = os.environ.get('RENDER_SUPERUSER_EMAIL')
        password = os.environ.get('RENDER_SUPERUSER_PASSWORD')

        # Only run if all env vars are present
        if not (username and email and password):
            return

        User = get_user_model()
        try:
            if not User.objects.filter(username=username).exists():
                User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                )
        except (OperationalError, ProgrammingError):
            # DB not ready during migrations/startup – ignore
            pass