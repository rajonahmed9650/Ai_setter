from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notifications


def create_notification(user, message, notif_type):
    """
    Always save notification in DB
    """
    return Notifications.objects.create(
        message=message,
        notif_type=notif_type,
        is_read=False
    )


def push_notification_if_allowed(user, message, notif_type):
    """
    Push only if user settings allow
    """
    settings = user.notificationsettings

    # settings OFF হলে push যাবে না
    if not getattr(settings, notif_type, False):
        print("🔕 PUSH BLOCKED BY SETTINGS")
        return
    print("🔔 PUSHING WEBSOCKET NOTIFICATION")
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        f"notifications_{user.id}",
        {
            "type": "send_notification",
            "message": message
        }
    )
