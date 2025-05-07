from fastapi import APIRouter, HTTPException, status, Request, Response
from fastapi.responses import StreamingResponse
import httpx
import os
import json
from datetime import datetime
from app.models import OpenAIRequest

router = APIRouter(prefix="/v1", tags=["openai proxy"])

# OpenAI API configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
OPENAI_API_BASE = "https://api.openai.com/v1"

# Mock database for API keys (replace with real DB in production)
from app.routes.api_keys import api_keys_db

def validate_api_key(api_key: str):
    """Validate the API key and update usage count"""
    if api_key not in api_keys_db:
        return False
    
    key_data = api_keys_db[api_key]
    
    # Check if key is active
    if not key_data["is_active"]:
        return False
    
    # Check if key is expired
    if datetime.utcnow() > key_data["expires_at"]:
        return False
    
    # Check if max usage is reached
    if key_data["max_usage"] and key_data["usage_count"] >= key_data["max_usage"]:
        return False
    
    # Update usage count
    api_keys_db[api_key]["usage_count"] += 1
    
    return True

@router.post("/chat/completions")
async def proxy_chat_completions(
    request: OpenAIRequest,
    api_key: str
):
    """Proxy endpoint for OpenAI chat completions API"""
    if not validate_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key"
        )
    
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI API key not configured"
        )
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{OPENAI_API_BASE}/chat/completions",
                json=request.dict(),
                headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
                timeout=60.0
            )
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from OpenAI API: {str(e)}"
        )

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_all(request: Request, path: str, api_key: str):
    """Generic proxy endpoint for all other OpenAI API endpoints"""
    if not validate_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key"
        )
    
    if not OPENAI_API_KEY:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI API key not configured"
        )
    
    try:
        # Get request body if any
        body = None
        if request.method in ["POST", "PUT"]:
            body = await request.json()
        
        # Prepare headers
        headers = dict(request.headers)
        headers["Authorization"] = f"Bearer {OPENAI_API_KEY}"
        
        # Remove host header to avoid conflicts
        if "host" in headers:
            del headers["host"]
        
        # Make request to OpenAI API
        url = f"{OPENAI_API_BASE}/{path}"
        
        async with httpx.AsyncClient() as client:
            response = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                json=body,
                params=request.query_params,
                timeout=60.0
            )
            
            return Response(
                content=response.content,
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from OpenAI API: {str(e)}"
        )
