import requests

BOT_URL = "http://172.252.13.97:8024/process-message"

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
            timeout=10
        )
        response.raise_for_status()
        return response.json()

    except requests.exceptions.RequestException as e:
        # log this
        print("Bot error:", str(e))
        return {
            "reply": "Sorry, something went wrong. Please try again later.",
            "next_state": current_state,
            "extracted_attributes": {}
        }