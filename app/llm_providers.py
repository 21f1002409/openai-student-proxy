
from typing import Dict, Any
import os
import litellm
from litellm import completion

# Configure LiteLLM with API keys from environment variables
litellm.api_key = {
    "openai": os.environ.get("OPENAI_API_KEY", ""),
    "anthropic": os.environ.get("ANTHROPIC_API_KEY", ""),
    "google": os.environ.get("GOOGLE_API_KEY", ""),
    "mistral": os.environ.get("MISTRAL_API_KEY", ""),
    "bedrock": os.environ.get("AWS_BEDROCK_ACCESS_KEY", "")
}

# Model mapping configuration
MODEL_MAPPING = {
    "gpt-3.5-turbo": "openai/gpt-3.5-turbo",
    "gpt-4": "openai/gpt-4",
    "claude-3-opus": "anthropic/claude-3-opus-20240229",
    "claude-3-sonnet": "anthropic/claude-3-sonnet-20240229",
    "claude-3-haiku": "anthropic/claude-3-haiku-20240307",
    "gemini-pro": "google/gemini-pro",
    "mistral-small": "mistral/mistral-small-latest",
    "mistral-medium": "mistral/mistral-medium-latest",
    "mistral-large": "mistral/mistral-large-latest",
    "claude-instant": "bedrock/anthropic.claude-instant-v1",
    "llama2": "bedrock/meta.llama2-13b-chat-v1"
}

async def process_llm_request(request_data: Dict[str, Any]) -> Dict[str, Any]:
    provider = request_data.get("provider", "openai")
    model_name = request_data.get("model")
    if model_name in MODEL_MAPPING:
        model_name = MODEL_MAPPING[model_name]
    elif "/" not in model_name:
        model_name = f"{provider}/{model_name}"
    try:
        response = completion(
            model=model_name,
            messages=request_data.get("messages", []),
            temperature=request_data.get("temperature", 0.7),
            max_tokens=request_data.get("max_tokens"),
            top_p=request_data.get("top_p", 1.0),
            frequency_penalty=request_data.get("frequency_penalty", 0.0),
            presence_penalty=request_data.get("presence_penalty", 0.0),
            stop=request_data.get("stop"),
            stream=request_data.get("stream", False)
        )
        return response
    except Exception as e:
        print(f"Error processing LLM request: {str(e)}")
        raise e
