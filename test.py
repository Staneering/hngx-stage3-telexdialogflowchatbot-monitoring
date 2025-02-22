import os
from google.cloud import dialogflow_v2
from google.cloud.dialogflow_v2 import SessionsClient
from google.cloud.dialogflow_v2.types import TextInput, QueryInput
import json

def setup_credentials():
    creds_path = os.path.join(os.path.dirname(__file__), 'service_account.json')
    print(creds_path)
    if not os.path.exists(creds_path):
        raise FileNotFoundError(f"Service account file not found at: {creds_path}")
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
    return creds_path

def setup_credentials_two():
    try:
        creds_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'service_account.json'))
        print(f'Looking for credentials at: {creds_path}')
        
        if not os.path.exists(creds_path):
            raise FileNotFoundError(f"Service account file not found at: {creds_path}")
        
        # Read project_id from service account file
        with open(creds_path, 'r', encoding='utf-8') as f:
            creds_data = json.load(f)
            project_id = creds_data.get('project_id')
            if not project_id:
                raise ValueError("No project_id found in service account file")
        
        # Set both environment variables
        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = creds_path
        os.environ["DIALOGFLOW_PROJECT_ID"] = project_id
        
        print(f"Project ID set to: {project_id}")
        return creds_path
    except json.JSONDecodeError as je:
        print(f"Error reading JSON file: {je}")
        raise
    except Exception as e:
        print(f"Unexpected error in setup_credentials: {e}")
        raise

def verify_credentials():
    try:
        creds_path = setup_credentials_two()
        client = dialogflow_v2.AgentsClient()
        print(f"Credentials verified successfully!")
        print(f"Using credentials from: {creds_path}")
    except Exception as e:
        print(f"Error verifying credentials: {e}")

def detect_intent_text(text: str, language_code: str = "en") -> dict:
    """
    Send a text query to Dialogflow and get the response.
    Args:
        text: User's input text
        language_code: Language code (default: "en")
    Returns:
        dict: Response from the agent
    """
    try:
        project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        if not project_id:
            raise ValueError("DIALOGFLOW_PROJECT_ID not set")

        session_client = SessionsClient()
        session = session_client.session_path(project_id, "test_session")
        
        text_input = TextInput(text=text, language_code=language_code)
        query_input = QueryInput(text=text_input)
        
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        
        return {
            "query_text": response.query_result.query_text,
            "intent": response.query_result.intent.display_name,
            "confidence": response.query_result.intent_detection_confidence,
            "response": response.query_result.fulfillment_text
        }
    except Exception as e:
        print(f"Error in detect_intent_text: {e}")
        raise

def detect_intent_text(text: str, language_code: str = "en") -> dict:
    """
    Send a text query to Dialogflow and get the response with detailed information.
    Args:
        text: User's input text
        language_code: Language code (default: "en")
    Returns:
        dict: Detailed response from the agent
    """
    try:
        project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
        if not project_id:
            raise ValueError("DIALOGFLOW_PROJECT_ID not set")

        session_client = SessionsClient()
        session = session_client.session_path(project_id, "test_session")
        
        text_input = TextInput(text=text, language_code=language_code)
        query_input = QueryInput(text=text_input)
        
        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )
        
        # Enhanced response dictionary with more details
        return {
            "query_text": response.query_result.query_text,
            "intent": response.query_result.intent.display_name,
            "confidence": response.query_result.intent_detection_confidence,
            "response": response.query_result.fulfillment_text,
            "parameters": dict(response.query_result.parameters),
            "all_required_params_present": response.query_result.all_required_params_present,
            "output_contexts": [
                {
                    "name": context.name,
                    "lifespan_count": context.lifespan_count,
                    "parameters": dict(context.parameters)
                }
                for context in response.query_result.output_contexts
            ]
        }
    except Exception as e:
        print(f"Error in detect_intent_text: {e}")
        raise

def chat_with_agent():
    """Interactive chat session with the Dialogflow agent with detailed responses."""
    try:
        verify_credentials()
        print("\nEnhanced Chat session started (type 'quit' to exit)")
        print("Type 'debug' to see full response details")
        print("Type 'train' to log unknown queries")
        print("-" * 50)
        
        debug_mode = False
        unknown_queries = []
        
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ['quit', 'exit', 'bye']:
                print("Chatbot: Goodbye!")
                break
            
            if user_input.lower() == 'debug':
                debug_mode = not debug_mode
                print(f"Debug mode: {'ON' if debug_mode else 'OFF'}")
                continue
                
            if user_input.lower() == 'train':
                if unknown_queries:
                    print("\nQueries that need training:")
                    for query in unknown_queries:
                        print(f"- '{query}'")
                else:
                    print("\nNo queries logged for training yet.")
                continue
                
            response = detect_intent_text(user_input)
            print(f"\nChatbot: {response['response']}")
            
            # Track fallback intents
            if response['intent'] == 'Default Fallback Intent':
                unknown_queries.append(user_input)
            
            if debug_mode:
                print("\nDEBUG INFO:")
                print(f"Intent: {response['intent']}")
                print(f"Confidence: {response['confidence']:.2f}")
                print(f"Parameters: {response['parameters']}")
                
            print("-" * 50)
            
    except Exception as e:
        print(f"Error in chat session: {e}")

        
def list_agents():
    try:
        client = dialogflow_v2.AgentsClient()
        parent = f"projects/{os.getenv('DIALOGFLOW_PROJECT_ID')}"
        # Initialize request argument(s)
        request = dialogflow_v2.SearchAgentsRequest(
        parent = f"projects/{os.getenv('DIALOGFLOW_PROJECT_ID')}",
        )

        # Make the request
        agents = client.search_agents(request=request)
        #agents = client.list_agents(request={"parent": parent})
        print("Available agents:")
        for agent in agents:
            print(f"- {agent.display_name}")
    except ValueError as ve:
        print(f"Configuration error: {ve}")
    except Exception as e:
        print(f"Error listing agents: {e}")



if __name__ == "__main__":
    verify_credentials()
    list_agents()
    chat_with_agent()