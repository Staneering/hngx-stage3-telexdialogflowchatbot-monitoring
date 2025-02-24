import requests
import os
#from config import TELEX_WEBHOOK_URL

def send_to_telex(response, response_time):
    """Send chatbot performance data to Telex channel."""
    payload = {
        "message": f"🤖 **Chatbot Performance Report**:\n📌 **Response**: {response}\n⏱️ **Response Time**: {response_time} sec",
        "channel": "chatbot-monitoring",
        "event_name": "chatbot-performance",
        "username": "Chatbot Monitor",
        "status": "success"
    }
    response = requests.post(os.getenv("TELEX_WEBHOOK_URL"), json=payload)
    return response.status_code, response.text

