from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notifications


def create_notification(client, message):
    return Notifications.objects.create(
        client_id=client,
        message=message,
        is_read=False
    )


def push_notification_if_allowed(user, client, message, notif_type):
    print("🚀 push_notification_if_allowed CALLED FOR USER:", user)

    settings = user.notifications_settings  # ✅ correct relation

    if not getattr(settings, notif_type, False):
        print("🔕 PUSH BLOCKED BY SETTINGS")
        return

    print("🔔 PUSHING WEBSOCKET NOTIFICATION")

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_client_{client.external_id}",  # ✅ matches WS
        {
            "type": "send_notification",
            "message": message
        }
    )
