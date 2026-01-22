import requests

BOT_URL = "http://172.252.13.97:8024/process-message"

def send_to_bot(client_id, message, current_state, user_attributes):
    """
    Sends message to external bot service
    """

    payload = {
        "user_id": f"client_{client_id}",
        "message": message,
        "current_state": current_state,
        "user_attributes": user_attributes,
    }

    response = requests.post(
        BOT_URL,
        json=payload,
    )
    response.raise_for_status()
    return response.json()
