from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.core.signals import request_finished
from django.dispatch import receiver

from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

channel_layer = get_channel_layer()


@receiver(post_save, sender=get_user_model())
def send_confirmation_email(sender, instance, created, **kwargs):
    user = instance
    if created and not user.email_confirmed:
        async_to_sync(channel_layer.send)(
            "confirmation_email", {"type": "send_email", "user_id": user.id}
        )