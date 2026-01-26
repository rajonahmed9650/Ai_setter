import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings

from clients.views import MessageView
from clients.webhooks.facebook_sender import send_facebook_reply


class FacebookWebhookView(APIView):
    permission_classes = [AllowAny]

    # 🔐 Verification
    def get(self, request):
        if (
            request.GET.get("hub.mode") == "subscribe"
            and request.GET.get("hub.verify_token") == settings.FB_VERIFY_TOKEN
        ):
            return Response(request.GET.get("hub.challenge"))
        return Response(status=403)

    # 📩 Receive messages
    def post(self, request):
        for entry in request.data.get("entry", []):
            for event in entry.get("messaging", []):

                if "message" not in event:
                    continue

                sender_id = event["sender"]["id"]
                text = event["message"].get("text")
                if not text:
                    continue

                payload = {
                    "external_id": sender_id,
                    "platform": "facebook",
                    "message": text
                }

                view = MessageView.as_view()
                response = view(
                    request._request.__class__(
                        request._request.environ,
                        body=json.dumps(payload).encode()
                    )
                )

                bot_reply = response.data.get("reply")
                if bot_reply:
                    send_facebook_reply(sender_id, bot_reply)

        return Response({"status": "ok"})
