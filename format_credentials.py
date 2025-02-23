import json

def format_credentials():
    # Read the service account file
    with open('service_account.json', 'r') as f:
        creds = json.load(f)
    
    # Convert to properly escaped JSON string
    json_str = json.dumps(creds)
    
    # Write to .env file
    with open('.env', 'w') as f:
        f.write(f'DIALOGFLOW_PROJECT_ID=dialogflowproject-451421\n')
        f.write(f'GOOGLE_APPLICATION_CREDENTIALS=service_account.json\n')
        f.write(f'GOOGLE_CREDENTIALS_JSON={json_str}\n')
        f.write(f'TELEX_WEBHOOK_URL=https://ping.telex.im/v1/webhooks/0195225b-a295-7cda-b277-58799168510a\n')
        f.write(f'CHATBOT_API=dialogflow\n')

if __name__ == "__main__":
    format_credentials()