import requests
import time    
from django.conf import settings

def send_facebook_dm(recipient_id, text):

    words = len(text.split())

    if words <= 10:
        time.sleep(4)
    elif words <= 15:
        time.sleep(6)
    elif words <= 30:
        time.sleep(10)
    else:
        time.sleep(15)


    url = "https://graph.facebook.com/v18.0/me/messages"

    payload = {
        "recipient": {"id": recipient_id},
        "message": {"text": text},
        "messaging_type": "RESPONSE"
    }

    params = {
        "access_token": settings.FB_PAGE_ACCESS_TOKEN
    }

    requests.post(url, params=params, json=payload)





def reply_to_comment(comment_id, text):
    url = f"https://graph.facebook.com/v18.0/{comment_id}/comments"
    params = {"access_token": settings.FB_PAGE_ACCESS_TOKEN}
    payload = {"message": text}
    requests.post(url, params=params, json=payload, timeout=10)
    # print("FB COMMENT REPLY STATUS:", res.status_code)
    # print("FB COMMENT REPLY BODY:", res.text)
   
def send_facebook_reply(target_id, text, reply_type="dm"):
    if reply_type == "dm":
        send_facebook_dm(target_id, text)
    elif reply_type == "comment":
        reply_to_comment(target_id, text)