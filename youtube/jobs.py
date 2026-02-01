# youtube/jobs.py
from rest_framework.test import APIRequestFactory
import time


def youtube_comment_job():
    # SAFE IMPORTS
    from django.contrib.auth.models import AnonymousUser
    from clients.views import MessageView
    from youtube.services.fetch_comments import fetch_latest_comments
    from youtube.services.reply import send_youtube_comment_reply
    from conversation.models import Conversation,Message

    factory = APIRequestFactory()
    comments = fetch_latest_comments()

    for c in comments:
        comment_id = c["comment_id"]

        # 🔥 DUPLICATE CHECK
        already_processed = Message.objects.filter(
            platform="youtube",
            external_comment_id=comment_id,
            sender_type="client"
        ).exists()

        if already_processed:
            print("⏩ Skipping already processed comment:", comment_id)
            continue

        payload = {
            "external_id": c["author_channel_id"],
            "message": c["text"],
            "platform": "youtube",
            "comment_id": comment_id,
            "sender_name": c["author_name"],
            "page_id": c["channel_id"],
        }

        fake_request = factory.post(
            "/api/message/",
            payload,
            format="json"
        )
        fake_request.user = AnonymousUser()

        #  trigger MessageView (this starts debounce thread)
        MessageView.as_view()(fake_request)

        #  WAIT for debounce + bot processing
        time.sleep(6)  # must be > DEBOUNCE_SECONDS

        #  fetch reply from DB
        conversation = (
            Conversation.objects
            .filter(
                source_id__platform="youtube",
                lead_id__client_id__external_id=c["author_channel_id"]
            )
            .order_by("-updated_at")
            .first()
        )


        reply_text = conversation.last_message if conversation else None
        print(" AI REPLY FROM DB:", reply_text)

        #  REAL YOUTUBE REPLY
        if reply_text:
            print(" SENDING YOUTUBE COMMENT REPLY")
            send_youtube_comment_reply(
                parent_comment_id=c["comment_id"],
                text=reply_text
            )
