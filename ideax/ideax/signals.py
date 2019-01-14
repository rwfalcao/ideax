from django.db.models.signals import post_save
from notifications.signals import notify
from .models import Popular_Vote


def my_handler(sender, instance, created, **kwargs):
    notify.send(instance, verb='liked')


post_save.connect(my_handler, sender=Popular_Vote)
