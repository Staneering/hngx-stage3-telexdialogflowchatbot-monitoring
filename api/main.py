from fastapi import FastAPI, Request
from utils.chatbot_api import query_dialogflow
from utils.telex_api import send_to_telex
from typing import Dict, Any
from pydantic import BaseModel

class ChatMessage(BaseModel):
    message: str

app = FastAPI(
    title="Chatbot Monitoring API",
    description="API for monitoring chatbot responses and performance"
)

def get_setting_value(settings: list, label: str, default: Any = None) -> Any:
    """Helper to extract setting value"""
    for setting in settings:
        if setting["label"] == label:
            return setting.get("default", default)
    return default

@app.get("/")
async def home():
    return {"message": "Telex Chatbot Monitoring is Running!"}

@app.post("/webhook")
async def process_message(request: Request):
    try:
        data = await request.json()
        
        # Extract settings from request
        settings = data.get("settings", [])
        message = data.get("message", "")
        
        # Get settings defined in integration.json
        project_id = get_setting_value(settings, "DIALOGFLOW_PROJECT_ID")
        credentials_json = get_setting_value(settings, "GOOGLE_CREDENTIALS_JSON")
        chatbot_api = get_setting_value(settings, "CHATBOT_API", "dialogflow")

        # Query Dialogflow
        response_text, response_time = query_dialogflow(
            text=message,
            project_id=project_id,
            credentials_json=credentials_json
        )

        # Send report to Telex
        telex_status, telex_response = send_to_telex(response_text, response_time)

        # Prepare response
        return {
            "event_name": "message_processed",
            "message": response_text,
            "status": telex_status,
            "username": "Dialogflow Bot",
            "metrics": {
                "response_time": response_time,
                "telex_status": telex_status
            }
        }

    except Exception as e:
        return {
            "event_name": "message_processed",
            "message": f"Error processing message: {str(e)}",
            "status": "error",
            "username": "Dialogflow Bot"
        }

# Keep the original endpoint for backward compatibility
@app.post("/chatbot-monitoring")
async def chatbot_monitoring(chat_message: ChatMessage):
    """
    Send a message to the chatbot and monitor its response.
    """
    response, response_time = query_dialogflow(chat_message.message)
    telex_status, telex_response = send_to_telex(response, response_time)

    return {
        "status": "processed",
        "chatbot_response": response,
        "response_time": response_time,
        "telex_status": telex_status
    }