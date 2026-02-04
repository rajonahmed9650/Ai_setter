import requests
import os
from dotenv import load_dotenv

load_dotenv()

BOT_URL = os.getenv("BOT_URL")

def send_to_bot(client_id, message, current_state, user_attributes):
    payload = {
        "user_id": f"client_{client_id}",
        "message": message,
        "current_state": current_state,
        "user_attributes": user_attributes,
    }

    try:
        response = requests.post(
            BOT_URL,
            json=payload,
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        # log this
        print("Bot error:", str(e))
        return {
            "reply": "Sorry,",
            "next_state": current_state,
            "extracted_attributes": {}
        }
    

# COMMENT_BOT_URL = os.getenv("COMMENT_BOT_URL")
COMMENT_BOT_URL ="http://172.252.13.97:8024/process-comment"

def send_to_comment_bot(platform, user_id, comment_text):
    payload = {
        "platform": platform.upper(),
        "user_id": user_id,
        "comment_text": comment_text,
    }

    response = requests.post(
        COMMENT_BOT_URL,
        json=payload,
        timeout=8
    )
    response.raise_for_status()
    return response.json()    





def route_bot(*, source, client, message, conversation):
    # 🟣 COMMENT BOT
    if source.source_type == "post_comment":
        return send_to_comment_bot(
            platform=source.platform,
            user_id=client.external_id,
            comment_text=message
        )

    # 🔵 DM BOT
    return send_to_bot(
        client_id=client.external_id,
        message=message,
        current_state=conversation.current_state,
        user_attributes=conversation.user_attributes,
    )