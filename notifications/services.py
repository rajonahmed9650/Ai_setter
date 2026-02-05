from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.contrib.auth.models import AnonymousUser

from .models import Notifications


def handle_new_lead(client, user, source, text):
    print("🚀 handle_new_lead CALLED")
    print("   user:", user)
    print("   client:", client)
    print("   source:", source)
    print("   text:", text[:50])

    # 1️⃣ Webhook / Postman safe guard
    if isinstance(user, AnonymousUser):
        print("⛔ RETURN: user is AnonymousUser")
        return

    # 2️⃣ Notification settings exists?
    if not hasattr(user, "notifications_settings"):
        print("⛔ RETURN: user has no notifications_settings")
        return

    settings = user.notifications_settings
    print("✅ settings found:", settings)

    # 3️⃣ Permission check
    if not settings.new_lead:
        print("⛔ RETURN: settings.new_lead is False")
        return

    print("✅ settings.new_lead = True")

    # 4️⃣ Message prepare
    msg = f"New DM from {source.platform.capitalize()}: {text[:80]}"
    print("📝 notification message:", msg)

    # 5️⃣ DB save
    notif = Notifications.objects.create(
        client_id=client,
        message=msg,
        is_read=False
    )
    print("💾 Notification saved in DB, id:", notif.id)

    # 6️⃣ WebSocket push
    channel_layer = get_channel_layer()
    print("📡 channel_layer:", channel_layer)

    async_to_sync(channel_layer.group_send)(
        f"notifications_client_{client.external_id}",
        {
            "type": "send_notification",
            "message": msg
        }
    )

    print("🔔 WebSocket notification SENT")
