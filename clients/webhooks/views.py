from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory

from clients.views import MessageView


class FacebookWebhookView(APIView):
    permission_classes = [AllowAny]

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

    def post(self, request):

        print(request.data)

        factory = APIRequestFactory()

        for entry in request.data.get("entry", []):
            for event in entry.get("messaging", []):
                message = event.get("message")
                if not message or message.get("is_echo"):
                    continue

                payload = {
                    "external_id": event["sender"]["id"],
                    "platform": "facebook",
                    "message": message.get("text"),
                    "page_id": event["recipient"]["id"],
                }

                fake_request = factory.post(
                    "/api/message/",
                    payload,
                    format="json"
                )
                fake_request.user = request.user

                # NO REPLY HERE
                MessageView.as_view()(fake_request)

        return Response({"status": "ok"})
