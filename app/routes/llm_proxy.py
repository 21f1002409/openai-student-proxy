
from fastapi import APIRouter, HTTPException, status
from fastapi import Request, Response
from app.models import LLMRequest
from app.llm_providers import process_llm_request
from app.routes.api_keys import validate_api_key

router = APIRouter(prefix="/v1", tags=["llm proxy"])

@router.post("/chat/completions")
async def proxy_chat_completions(request: LLMRequest, api_key: str):
    if not validate_api_key(api_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired API key"
        )
    try:
        response = await process_llm_request(request.dict())
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error from LLM API: {str(e)}"
        )
