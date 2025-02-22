import os
import json
import time
from typing import Tuple, Dict, Any
from google.cloud import dialogflow
from google.cloud.dialogflow_v2.types import TextInput, QueryInput
from google.oauth2 import service_account
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def get_credentials(credentials_json: str = None):
    """Get credentials from environment variable or passed JSON"""
    try:
        if credentials_json:
            creds_dict = json.loads(credentials_json)
        else:
            creds_dict = json.loads(os.getenv('GOOGLE_CREDENTIALS_JSON', '{}'))
        return service_account.Credentials.from_service_account_info(creds_dict)
    except Exception as e:
        raise RuntimeError(f"Failed to load credentials: {e}")

def query_dialogflow(
    text: str, 
    project_id: str = None,
    credentials_json: str = None,
    session_id: str = "test_session", 
    language_code: str = "en"
) -> Tuple[str, float]:
    """
    Send a message to Dialogflow and get the response.
    
    Args:
        text: The user's input text
        project_id: Dialogflow project ID (optional)
        credentials_json: Service account credentials JSON (optional)
        session_id: Session identifier (default: "test_session")
        language_code: Language code (default: "en")
        
    Returns:
        Tuple containing:
        - Response text
        - Response time in seconds
    """
    try:
        start_time = time.time()

        # Get credentials
        credentials = get_credentials(credentials_json)
        
        # Initialize client
        client = dialogflow.SessionsClient(credentials=credentials)
        
        # Use provided project ID or fall back to environment variable
        project_id = project_id or os.getenv('DIALOGFLOW_PROJECT_ID')
        if not project_id:
            raise ValueError("Project ID not provided")
            
        session = client.session_path(project_id, session_id)
        
        text_input = TextInput(text=text, language_code=language_code)
        query_input = QueryInput(text=text_input)
        
        response = client.detect_intent(session=session, query_input=query_input)
        
        end_time = time.time()
        response_time = round(end_time - start_time, 2)

        return (
            response.query_result.fulfillment_text,
            response_time
        )

    except Exception as e:
        print(f"Error in query_dialogflow: {e}")
        raise