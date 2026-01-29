from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import AnonymousUser

from .models import Notifications


def handle_new_lead(client, user, source, text):
    # ✅ FIX: Webhook / Postman safe guard
    if isinstance(user, AnonymousUser):
        return

    # Extra safety (optional but good)
    if not hasattr(user, "notifications_settings"):
        return

    settings = user.notifications_settings

    if not settings.new_lead:
        return

    msg = f"New DM from {source.platform.capitalize()}: {text[:80]}"

    Notifications.objects.create(
        client_id=client,
        message=msg,
        is_read=False
    )

    # Realtime notification (WebSocket)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_client_{client.external_id}",
        {
            "type": "send_notification",
            "message": msg
        }
    )
