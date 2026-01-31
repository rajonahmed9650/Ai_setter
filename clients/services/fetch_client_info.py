# services/facebook.py
import requests
from django.conf import settings

def fetch_sender_name(sender_id):
    """
    Facebook / Instagram Business DM sender name fetch করে
    """
    url = f"https://graph.facebook.com/v18.0/{sender_id}"
    params = {
        "fields": "name",
        "access_token": settings.FB_PAGE_ACCESS_TOKEN
    }

    response = requests.get(url, params=params, timeout=15)

    if response.status_code == 200:
        data = response.json()
        return data.get("name")

    return None
