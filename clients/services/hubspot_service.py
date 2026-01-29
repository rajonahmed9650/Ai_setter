import requests
from django.conf import settings

HUBSPOT_URL = "https://api.hubapi.com/crm/v3/objects/contacts"

def sync_lead_to_hubspot(lead):
    client = lead.client_id

    headers = {
        "Authorization": f"Bearer {settings.HUBSPOT_ACCESS_TOKEN}",
        "Content-Type": "application/json",
    }

    payload = {
        "properties": {
            "external_id": client.external_id,
            "lead_score": str(lead.score),
            "lead_status": lead.status,
        }
    }

    response = requests.post(
        HUBSPOT_URL,
        headers=headers,
        json=payload,
        timeout=10
    )

    if response.status_code in (200, 201):
        print("✅ HubSpot contact synced")
        return True

    print("❌ HubSpot error:", response.status_code, response.text)
    return False
