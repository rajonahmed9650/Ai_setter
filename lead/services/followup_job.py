from django.utils import timezone
from conversation.models import Conversation, Message
from lead.services.followup_rules import FOLLOWUP_RULES
from clients.webhooks.facebook_sender import send_facebook_reply



# def booking_link_already_sent(convo):
#     """
#     Returns True if booking link already sent in this conversation
#     """

#     return Message.objects.filter(
#         conversation_id=convo,
#         sender_type="bot"
#     ).filter(
#         # Option 1: structured way
#         message__type="booking_link"
#     ).exists()


# def booking_link_already_sent(convo):
#     return Message.objects.filter(
#         conversation_id=convo,
#         sender_type="bot",
#         message__text__icontains="http"
#     ).exists()


def followup_job():
    try:
        now = timezone.now()
        print("\n🔥 FOLLOWUP JOB RUNNING:", now)

        conversations = Conversation.objects.filter(
            lead_id__status__in=["nature", "warm lead", "hot lead"]
        )

        print("📊 TOTAL CONVERSATIONS:", conversations.count())

        for convo in conversations:
            print("\n🔁 CONVO ID:", convo.id)

            lead = convo.lead_id
            print("LEAD SCORE:", lead.score)

            print("SOURCE PLATFORM:", convo.source_id.platform)
            print("SOURCE TYPE:", getattr(convo.source_id, "source_type", "❌"))

            # DM only
            if convo.source_id.platform not in ["facebook", "instagram"]:
                print("⏩ SKIP: not DM")
                continue

            last_client_msg = Message.objects.filter(
                conversation_id=convo,
                sender_type="client"
            ).order_by("-created_at").first()

            print("LAST CLIENT MSG:", last_client_msg)

            if not last_client_msg:
                print("⏩ SKIP: no client msg")
                continue

            already_followed = Message.objects.filter(
                conversation_id=convo,
                sender_type="bot",
                is_followup=True
            ).exists()

            print("ALREADY FOLLOWED:", already_followed)

            if already_followed:
                continue


            # if booking_link_already_sent(convo):
            #     print("⏩ SKIP: booking link already sent")
            #     continue

            for rule in FOLLOWUP_RULES:
                print("RULE:", rule)

                if rule["min"] <= lead.score <= rule["max"]:
                    due_time = last_client_msg.created_at + rule["delay"]

                    print("NOW:", now)
                    print("DUE:", due_time)

                    if now < due_time:
                        print("⏳ WAITING...")
                        continue

                    print("💾 SAVING FOLLOWUP")
                    Message.objects.create(
                        conversation_id=convo,
                        sender_type="bot",
                        is_followup=True,
                        message={
                            "text": rule["message"],
                            "followup": True
                        },
                        platform=convo.source_id.platform
                    )

                    print("📤 SENDING DM")
                    try:
                        send_facebook_reply(
                            convo.lead_id.client_id.external_id,
                            rule["message"],
                            reply_type="dm"
                        )
                    except Exception as e:
                        print("❌ FB ERROR:", e)

                    break

    except Exception as e:
        print("🔥 FOLLOWUP JOB CRASHED:", e)

