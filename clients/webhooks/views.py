import json
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponse

from clients.views import MessageView
from clients.webhooks.facebook_sender import send_facebook_reply
from rest_framework.test import APIRequestFactory


class FacebookWebhookView(APIView):
    permission_classes = [AllowAny]

    # Webhook Verification 
    def get(self, request):
        if (
            request.GET.get("hub.mode") == "subscribe"
            and request.GET.get("hub.verify_token") == settings.FB_VERIFY_TOKEN
        ):
            return HttpResponse(
                request.GET.get("hub.challenge"),
                content_type="text/plain"
            )

        return HttpResponse("Forbidden", status=403)

    # Receive messages (THIS PART IS OK)
    def post(self, request):
        print("🔥🔥 FACEBOOK WEBHOOK HIT 🔥🔥")
        print(request.data)
        factory = APIRequestFactory()

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

                fake_request = factory.post(
                    "/api/message/",
                    payload,
                    format="json"
                )
                fake_request.user = request.user

                response = MessageView.as_view()(fake_request)

                bot_reply = response.data.get("reply")
                if bot_reply:
                    send_facebook_reply(sender_id, bot_reply)

        return Response({"status": "ok"})
