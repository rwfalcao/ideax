from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class IdeaxConfig(AppConfig):
    name = 'ideax'

    def ready(self):
        from ideax.signals import check_user_profile
        user_logged_in.connect(check_user_profile)
