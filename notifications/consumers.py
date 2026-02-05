import json
from channels.generic.websocket import AsyncWebsocketConsumer

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        print("🔌 CONNECT HIT")
        print("CHANNEL LAYER:", self.channel_layer)
        self.client_id = self.scope["url_route"]["kwargs"]["client_id"]
        self.group_name = f"notifications_client_{self.client_id}"

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        if hasattr(self, "group_name"):
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )

    async def send_notification(self, event):
        await self.send(text_data=json.dumps({
            "type": "notification",
            "message": event["message"]
        }))
