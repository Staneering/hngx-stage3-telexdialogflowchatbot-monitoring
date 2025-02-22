from fastapi import FastAPI, Request
from pydantic import BaseModel
from utils.chatbot_api import query_dialogflow
from utils.telex_api import send_to_telex

class ChatMessage(BaseModel):
    message: str

app = FastAPI(
    title="Chatbot Monitoring API",
    description="API for monitoring chatbot responses and performance"
)

@app.get("/")
async def home():
    return {"message": "Telex Chatbot Monitoring is Running!"}

@app.post("/chatbot-monitoring")
async def chatbot_monitoring(chat_message: ChatMessage):
    """
    Send a message to the chatbot and monitor its response.
    
    Args:
        chat_message: The message to send to the chatbot
        
    Returns:
        dict: Contains the chatbot response, response time, and monitoring status
    """
    # Get response from Dialogflow
    response, response_time = query_dialogflow(chat_message.message)
    
    # Send report to Telex
    telex_status, telex_response = send_to_telex(response, response_time)

    return {
        "status": "processed",
        "chatbot_response": response,
        "response_time": response_time,
        "telex_status": telex_status
    }