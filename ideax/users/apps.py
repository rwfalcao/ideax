from django.apps import AppConfig
from django.contrib.auth.signals import user_logged_in


class UserConfig(AppConfig):
    name = 'ideax.users'

    def ready(self):
        from .signals import check_user_profile  # noqa
        from django.db.models.signals import post_migrate
        from ideax.users.signals import create_notice_types

        post_migrate.connect(create_notice_types, sender=self)
        user_logged_in.connect(check_user_profile)
