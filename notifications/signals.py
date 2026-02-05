from django.db.models.signals import post_save
from django.dispatch import receiver
from accounts.models import User
from .models import Notifications_settings

@receiver(post_save, sender=User)
def create_notification_settings(sender, instance, created, **kwargs):
    if created:
        Notifications_settings.objects.create(user_id=instance)
