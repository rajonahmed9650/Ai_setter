from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notifications

def handle_new_lead(client, user, source, text):
    settings = user.notifications_settings

    # 🔕 user OFF করলে push যাবে না
    if not settings.new_lead:
        return

    msg = f"New DM from {source.platform.capitalize()}: {text[:80]}"

    # ✅ DB save (always)
    Notifications.objects.create(
        client_id=client,
        message=msg,
        is_read=False
    )

    # 🔔 WebSocket push (client based)
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_client_{client.external_id}",
        {
            "type": "send_notification",
            "message": msg
        }
    )
