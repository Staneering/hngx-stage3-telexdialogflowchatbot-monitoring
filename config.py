import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# Fetch values
DIALOGFLOW_PROJECT_ID = os.getenv("DIALOGFLOW_PROJECT_ID")
GOOGLE_APPLICATION_CREDENTIALS = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
TELEX_WEBHOOK_URL = os.getenv("TELEX_WEBHOOK_URL")
CHATBOT_API = os.getenv("CHATBOT_API", "dialogflow")  # Default to Dialogflow
