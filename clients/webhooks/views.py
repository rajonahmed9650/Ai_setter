from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.conf import settings
from django.http import HttpResponse
from rest_framework.test import APIRequestFactory
from clients.views import MessageView
from clients.webhooks.facebook_sender import send_facebook_reply
from lead.services.bot_service import send_to_bot


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

        print("webhook hit")

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


            for change in entry.get("changes", []):
                value = change.get("value", {})

                if value.get("item") != "comment":
                    continue

                comment_id = value.get("comment_id")
                comment_text = value.get("message")
                from_user = value.get("from", {})
                user_id = from_user.get("id")
                user_name = from_user.get("name")

                if not comment_id or not comment_text or not user_id:
                    continue

                print("💬 NEW COMMENT:", comment_text)

                payload = {
                    "external_id": user_id,
                    "platform": "facebook_comment",
                    "message": comment_text,
                    "app_id": entry.get("id"),
                    "comment_id": comment_id,
                    "sender_name":user_name
                }

                fake_request = factory.post(
                    "/api/message/",
                    payload,
                    format="json"
                )
                fake_request.user = request.user

                MessageView.as_view()(fake_request)

   

        return Response({"status": "ok"})
