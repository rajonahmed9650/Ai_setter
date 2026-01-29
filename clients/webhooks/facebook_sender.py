import requests
import time    
from django.conf import settings

def send_facebook_reply(recipient_id, text):

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
