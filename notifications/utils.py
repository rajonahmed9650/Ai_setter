# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync
# from .models import Notifications


# def create_notification(client, message):
#     return Notifications.objects.create(
#         client_id=client,
#         message=message,
#         is_read=False
#     )


# def push_notification_if_allowed(user, client, message, notif_type):
#     print("🚀 push_notification_if_allowed CALLED FOR USER:", user)

#     settings = user.notifications_settings  # ✅ correct relation

#     if not getattr(settings, notif_type, False):
#         print("🔕 PUSH BLOCKED BY SETTINGS")
#         return

#     print("🔔 PUSHING WEBSOCKET NOTIFICATION")

#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         f"notifications_client_{client.external_id}",  # ✅ matches WS
#         {
#             "type": "send_notification",
#             "message": message
#         }
#     )





from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Notifications


def create_notification(client, message):
    return Notifications.objects.create(
        client_id=client,
        message=message,
        is_read=False
    )


def push_notification_if_allowed(user, client, lead, message, notif_type):
    """
    Push notification ONLY ONCE per new lead
    """

    print("🚀 push_notification_if_allowed CALLED FOR USER:", user)

    # 1️⃣ settings check
    settings = user.notifications_settings
    if not getattr(settings, notif_type, False):
        print("🔕 PUSH BLOCKED BY SETTINGS")
        return

    # 2️⃣ already notified? → STOP
    if lead.notification_sent:
        print("⏭️ Notification already sent for this lead")
        return

    # 3️⃣ create DB notification
    create_notification(client, message)

    # 4️⃣ GLOBAL websocket push
    print("🔔 PUSHING GLOBAL WEBSOCKET NOTIFICATION")

    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notifications_global",
        {
            "type": "send_notification",
            "message": message,
            "client_id": client.external_id,
        }
    )

    # 5️⃣ mark as sent
    lead.notification_sent = True
    lead.save(update_fields=["notification_sent"])
