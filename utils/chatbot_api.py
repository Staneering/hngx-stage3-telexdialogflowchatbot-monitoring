import os
import time
from typing import Tuple, Dict, Any
from google.cloud import dialogflow
from google.cloud.dialogflow_v2.types import TextInput, QueryInput
from google.oauth2 import service_account
import json

# Load environment variables
from config import DIALOGFLOW_PROJECT_ID, GOOGLE_APPLICATION_CREDENTIALS

# Load service account credentials from environment variable
try:
    service_account_info = json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON'))
    credentials = service_account.Credentials.from_service_account_info(service_account_info)
except Exception as e:
    raise RuntimeError(f"Failed to load credentials: {e}")

def query_dialogflow(text: str, session_id: str = "test_session", language_code: str = "en") -> Tuple[str, float, Dict[str, Any]]:
    """
    Send a message to Dialogflow and get the response.
    
    Args:
        text: The user's input text
        session_id: Session identifier (default: "test_session")
        
    Returns:
        Tuple containing:
        - Response text
        - Response time in seconds
        - Additional response details
    """
    try:
        start_time = time.time()

        client = dialogflow.SessionsClient(credentials=credentials)
        session = client.session_path(os.getenv("DIALOGFLOW_PROJECT_ID"), session_id)
        
        text_input = TextInput(text=text, language_code=language_code)
        query_input = QueryInput(text=text_input)
        
        response = client.detect_intent(session=session, query_input=query_input)
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)

        # Additional response details
        response_details = {
            "intent": response.query_result.intent.display_name,
            "confidence": response.query_result.intent_detection_confidence,
            "parameters": dict(response.query_result.parameters),
            "sentiment": getattr(response.query_result, 'sentiment_analysis_result', None)
        }

        return (
            response.query_result.fulfillment_text,
            response_time,
            #response_details
        )

    except Exception as e:
        print(f"Error in query_dialogflow: {e}")
        raise
