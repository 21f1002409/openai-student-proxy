
# LLM-Agnostic Student API Proxy

A serverless FastAPI application that provides temporary access to multiple LLM providers for students through a secure proxy.

## Features

- Support for multiple LLM providers (OpenAI, Anthropic, Google, Mistral, AWS Bedrock)
- User registration and authentication
- Temporary API key generation for students
- Proxy to LLM APIs with usage tracking
- Serverless deployment on AWS Lambda

## Supported LLM Providers

- OpenAI (GPT-3.5, GPT-4)
- Anthropic (Claude 3 Opus, Sonnet, Haiku)
- Google (Gemini Pro)
- Mistral AI (Small, Medium, Large)
- AWS Bedrock (Claude, Llama 2)

## Usage Example

```
import requests

API_KEY = "your-api-key"
API_URL = "https://your-api-gateway-url.amazonaws.com/v1/chat/completions"

# Using OpenAI's GPT-3.5
response = requests.post(
    API_URL,
    json={
        "provider": "openai",
        "model": "gpt-3.5-turbo",
        "messages": [{"role": "user", "content": "Hello, AI!"}]
    },
    params={"api_key": API_KEY}
)

print(response.json())

# Using Anthropic's Claude
response = requests.post(
    API_URL,
    json={
        "provider": "anthropic",
        "model": "claude-3-haiku",
        "messages": [{"role": "user", "content": "Hello, AI!"}]
    },
    params={"api_key": API_KEY}
)

print(response.json())
```

## Benefits of the LLM-Agnostic Approach

By implementing this LLM-agnostic architecture using LiteLLM, we've created several advantages:

1. **Flexibility**: Students can experiment with different LLM providers without changing their code
2. **Future-proofing**: New models can be added without modifying the core API
3. **Consistent interface**: All LLM providers are accessed through the same API format
4. **Simplified management**: API keys for different providers are managed in one place
5. **Educational value**: Students can compare different models' performance and characteristics

This implementation allows students to explore the strengths and weaknesses of different LLM providers while maintaining a consistent interface for their applications. The proxy handles the complexity of routing requests to the appropriate provider and formatting the responses in a standardized way.

The updated repository now provides a truly LLM-agnostic solution that will serve as an excellent educational tool for students learning about generative AI technologies.
