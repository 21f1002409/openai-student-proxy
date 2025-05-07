# OpenAI Student API Proxy

A serverless FastAPI application that provides temporary OpenAI API access to students through a secure proxy.

## Features

- User registration and authentication
- Temporary API key generation for students
- Proxy to OpenAI API with usage tracking
- Serverless deployment on AWS Lambda

## Setup and Deployment

### Prerequisites

- AWS Account
- Serverless Framework installed
- Python 3.9+
- OpenAI API Key

### Local Development

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate the virtual environment: 
   - Windows: `venv\Scripts\activate`
   - Unix/MacOS: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Set environment variables:
   - `export SECRET_KEY="your-secret-key"`
   - `export OPENAI_API_KEY="your-openai-api-key"`
6. Run the application: `uvicorn app.main:app --reload`

### Deployment

1. Configure AWS credentials for Serverless Framework
2. Deploy the application: `serverless deploy`

## Usage

### For Administrators

1. Deploy the application
2. Share the API endpoint with students

### For Students

1. Register an account at `/signup`
2. Login to get a JWT token at `/token`
3. Generate an API key at `/api-keys`
4. Use the API key to access OpenAI API through the proxy

Example request:

```
import requests

API_KEY = "your-api-key"
API_URL = "https://your-api-gateway-url.amazonaws.com/v1/chat/completions"

response = requests.post(
    API_URL,
    json={
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello, AI!"}]
    },
    params={"api_key": API_KEY}
)

print(response.json())
```

## Security Considerations

- Store secrets securely using AWS Secrets Manager
- Implement rate limiting
- Use a proper database instead of in-memory storage
- Set appropriate CORS policies in production

## License

MIT
