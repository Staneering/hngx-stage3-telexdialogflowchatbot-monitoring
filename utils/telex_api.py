import os
import requests
from typing import Tuple
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def send_to_telex(message: str, response_time: float) -> Tuple[str, dict]:
    """
    Send monitoring data to Telex webhook.
    """
    try:
        webhook_url = os.getenv('TELEX_WEBHOOK_URL')
        if not webhook_url:
            raise ValueError("Telex webhook URL not configured")

        payload = {
            "event_name": "message_processed",
            "message": message,
            "username": "Dialogflow Bot",
            "metrics": {
                "response_time": response_time
            }
        }

        response = requests.post(
            webhook_url,
            json=payload,
            headers={"Content-Type": "application/json"}
        )

        if response.status_code == 200:
            return "success", response.json()
        else:
            return "error", {
                "status_code": response.status_code,
                "error": "Failed to send to Telex"
            }

    except Exception as e:
        return "error", {"error": str(e)}
