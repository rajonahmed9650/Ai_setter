import requests
from django.conf import settings

def send_facebook_reply(recipient_id, text):
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
