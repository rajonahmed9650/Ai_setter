from django.core.cache import cache
import time
from threading import Thread
from django.utils import timezone
from conversation.models import Message
from lead.services.bot_service import send_to_bot
from notifications.services import handle_new_lead
from .hubspot_service import sync_lead_to_hubspot
from clients.webhooks.facebook_sender import send_facebook_reply
from youtube.services.reply import send_youtube_comment_reply

DEBOUNCE_SECONDS = 10    
BUFFER_TTL = 15


def buffer_message(platform, external_id, text):
    key = f"msg_buffer:{platform}:{external_id}"
    messages = cache.get(key, [])
    messages.append(text)
    cache.set(key, messages, timeout=BUFFER_TTL)


def acquire_debounce_lock(platform, external_id):
    lock_key = f"msg_lock:{platform}:{external_id}"
    if cache.get(lock_key):
        return False
    cache.set(lock_key, True, timeout=DEBOUNCE_SECONDS)
    return True


def delayed_process(platform, external_id, process_func):
    time.sleep(DEBOUNCE_SECONDS)

    buffer_key = f"msg_buffer:{platform}:{external_id}"
    lock_key = f"msg_lock:{platform}:{external_id}"

    messages = cache.get(buffer_key)
    if not messages:
        return

    combined_message = " ".join(messages)

    cache.delete(buffer_key)
    cache.delete(lock_key)

    process_func(combined_message)


def start_debounce(platform, external_id, process_func):
    if acquire_debounce_lock(platform, external_id):
        Thread(
            target=delayed_process,
            args=(platform, external_id, process_func),
            daemon=True
        ).start()





def process_combined_message(
    *,
    combined_text,
    external_id,
    source,
    client,
    lead,
    conversation,
    request_user,
    comment_id=None
):
    print("commet _id:",comment_id)
    print("🔥 process_combined_message CALLED")
    is_comment = bool(comment_id)

    

    #  Save client combined message
    Message.objects.create(
        conversation_id=conversation,
        sender_type="client",
        message={"text": combined_text},
        platform=source.platform,
        external_comment_id=comment_id 
    )



    handle_new_lead(
        client=client,
        user=request_user,
        source=source,
        text=combined_text
    )

    if is_comment:
        from lead.services.bot_service import send_to_comment_bot

        bot_response = send_to_comment_bot(
            platform=source.platform,
            user_id=external_id,
            comment_text=combined_text
        )
    else:
        bot_response = send_to_bot(
            client_id=external_id,
            message=combined_text,
            current_state=conversation.current_state,
            user_attributes=conversation.user_attributes,
        )

    print("🤖 BOT FULL RESPONSE =", bot_response)
    print("🤖 BOT REPLY =", bot_response.get("reply"))
    #  Save bot reply (DB)
    if not is_comment: 
        conversation.current_state = bot_response.get(
            "next_state",
            conversation.current_state
        )

        conversation.user_attributes.update(
            bot_response.get("extracted_attributes") or {}
        )

        conversation.last_message = bot_response.get("reply")
        conversation.save()

        #  Lead update
        progress_score = bot_response.get("progress_score", 0)
        lead.score = progress_score

        if progress_score >= 80:
            lead.status = "hot lead"
            sync_lead_to_hubspot(lead)
        elif progress_score >= 50:
            lead.status = "warm lead"
        else:
            lead.status = "nature"

        lead.last_response = timezone.now()
        lead.save()

    Message.objects.create(
        conversation_id=conversation,
        sender_type="bot",
        message=bot_response,
        platform=source.platform,
        external_comment_id=comment_id
    )


    if is_comment:
        reply_text = bot_response.get("reply_text")
    else:
        reply_text = bot_response.get("reply")


    if not reply_text or not reply_text.strip():
        print("⚠️ Empty reply — skipping send")
        return


    if comment_id:
        print("📤 SENDING COMMENT REPLY")
        send_facebook_reply(
            comment_id,          
            reply_text,
            reply_type="comment"
        )
    else:
        print("📤 SENDING DM REPLY")
        send_facebook_reply(
            external_id,        
            reply_text,
            reply_type="dm"
        )

    if source.platform == "youtube" and comment_id:
        print("📤 Sending YouTube comment reply")
        send_youtube_comment_reply(
            parent_comment_id=comment_id,
            text=reply_text
        )

    

