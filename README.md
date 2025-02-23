# Dialogflow Chatbot Monitoring

This project integrates a Dialogflow chatbot with performance monitoring and reporting capabilities. It uses FastAPI to create an API for sending messages to the chatbot and monitoring its responses. The performance data is sent to a Telex channel for further analysis.

## Features

- Dialogflow AI integration
- Response time tracking
- Performance monitoring
- Automatic responses
- Telex integration for performance reporting

## Requirements

- Python 3.7+
- FastAPI
- Google Cloud Dialogflow
- Telex

## Setup

1. **Clone the repository**:
   ```sh
   git clone https://github.com/telex-integrations/hngx-stage3-telexdialogflowchatbot-monitoring.git
   cd hngx-stage3-telexdialogflowchatbot-monitoring
   ```

2. **Create a virtual environment**:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```sh
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following content:
   ```properties
   DIALOGFLOW_PROJECT_ID=your-dialogflow-project-id
   GOOGLE_APPLICATION_CREDENTIALS=path-to-your-service-account.json
   GOOGLE_CREDENTIALS_JSON={"type": "service_account", "project_id": "your-dialogflow-project-id", "private_key_id": "your-private-key-id", "private_key": "your-private-key", "client_email": "your-client-email", "client_id": "your-client-id", "auth_uri": "https://accounts.google.com/o/oauth2/auth", "token_uri": "https://oauth2.googleapis.com/token", "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs", "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/your-client-email"}
   TELEX_WEBHOOK_URL=your-telex-webhook-url
   CHATBOT_API=dialogflow
   ```

5. **Run the application**:
   ```sh
   uvicorn api.main:app --reload
   ```

## Deployment on Render

1. **Create a new web service on Render**:
   - Go to the Render dashboard.
   - Click on "New" and select "Web Service".
   - Connect your GitHub repository and select the repository for this project.

2. **Configure the environment**:
   - Set the build and start commands:
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port 10000`
   - Add the following environment variables in the Render dashboard:
     - `DIALOGFLOW_PROJECT_ID`
     - `GOOGLE_CREDENTIALS_JSON`
     - `TELEX_WEBHOOK_URL`
     - `CHATBOT_API`

3. **Deploy the service**:
   - Click "Create Web Service" to deploy your application.

4. **Access your deployed application**:
   - Your application will be available at `https://hngx-stage3-telexdialogflowchatbot.onrender.com`.

## Endpoints

### Home

- **URL**: `/`
- **Method**: `GET`
- **Description**: Returns a message indicating that the Telex Chatbot Monitoring is running.

### Chatbot Monitoring

- **URL**: `/chatbot-monitoring`
- **Method**: `POST`
- **Description**: Sends a message to the chatbot and monitors its response.
- **Request Body**:
  ```json
  {
    "message": "Hello, chatbot!"
  }
  ```
- **Response**:
  ```json
  {
    "status": "processed",
    "chatbot_response": "Hello! How can I assist you today?",
    "response_time": 0.45,
    "telex_status": 200
  }
  ```

### Integrations

- **URL**: `/integrations.json`
- **Method**: `GET`
- **Description**: Returns the contents of the `integrations.json` file.

## Testing with Postman

1. **Open Postman**.
2. **Create a new request**.
3. **Set the request type to `POST`**.
4. **Enter the URL**: `https://hngx-stage3-telexdialogflowchatbot.onrender.com/chatbot-monitoring`.
5. **Set Headers**:
   - Key: `Content-Type`
   - Value: `application/json`
6. **Set the Body**:
   - Select `raw`.
   - Choose `JSON` from the dropdown.
   - Enter your JSON payload:
     ```json
     {
       "message": "Hello, chatbot!"
     }
     ```
7. **Send the request** and view the response.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.