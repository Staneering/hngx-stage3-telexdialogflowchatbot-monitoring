import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Configuration settings for the application"""
    
    # Dialogflow settings
    DIALOGFLOW_PROJECT_ID: str = os.getenv('DIALOGFLOW_PROJECT_ID', '')
    GOOGLE_CREDENTIALS_JSON: str = os.getenv('GOOGLE_CREDENTIALS_JSON', '{}')
    GOOGLE_APPLICATION_CREDENTIALS: str = os.getenv('GOOGLE_APPLICATION_CREDENTIALS', 'service_account.json')
    
    # Telex settings
    TELEX_WEBHOOK_URL: str = os.getenv('TELEX_WEBHOOK_URL', '')
    CHATBOT_API: str = os.getenv('CHATBOT_API', 'dialogflow')
    
    # API settings
    API_TITLE: str = "Chatbot Monitoring API"
    API_DESCRIPTION: str = "API for monitoring chatbot responses and performance"
    API_VERSION: str = "1.0.0"
    
    # Bot settings
    BOT_NAME: str = "Dialogflow Bot"
    DEFAULT_SESSION_ID: str = "test_session"
    DEFAULT_LANGUAGE_CODE: str = "en"

    @classmethod
    def get_settings(cls) -> dict:
        """Get all settings as a dictionary"""
        return {
            "project_id": cls.DIALOGFLOW_PROJECT_ID,
            "webhook_url": cls.TELEX_WEBHOOK_URL,
            "chatbot_api": cls.CHATBOT_API,
            "bot_name": cls.BOT_NAME
        }

# Create settings instance
settings = Settings()