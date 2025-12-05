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

        # If any of them is missing, do nothing
        if not (username and email and password):
            return

        # You can hardcode first/last name or later put them in env vars too
        first_name = "Admin"
        last_name = "User"

        User = get_user_model()
        try:
            if not User.objects.filter(username=username).exists():
                # IMPORTANT: pass all required fields with correct names
                User.objects.create_superuser(
                    first_name=first_name,
                    last_name=last_name,
                    email=email,
                    username=username,
                    password=password,
                )
        except (OperationalError, ProgrammingError):
            # DB not ready yet – ignore
            pass