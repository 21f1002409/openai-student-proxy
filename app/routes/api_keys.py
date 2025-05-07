from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime, timedelta
from app.models import User, ApiKey, ApiKeyResponse
from app.auth import get_current_active_user

router = APIRouter(prefix="/api-keys", tags=["api keys"])

# Mock database for API keys (replace with real DB in production)
api_keys_db = {}

@router.post("", response_model=ApiKeyResponse)
async def create_api_key(
    days_valid: int = 7, 
    max_usage: int = None,
    current_user: User = Depends(get_current_active_user)
):
    """Generate a new API key for the authenticated user"""
    if days_valid <= 0 or days_valid > 30:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Days valid must be between 1 and 30"
        )
    
    expires_at = datetime.utcnow() + timedelta(days=days_valid)
    
    api_key = ApiKey(
        user_id=current_user.id,
        expires_at=expires_at,
        max_usage=max_usage
    )
    
    # Store in database
    api_keys_db[api_key.key] = api_key.dict()
    
    return ApiKeyResponse(
        key=api_key.key,
        expires_at=api_key.expires_at,
        created_at=api_key.created_at,
        max_usage=api_key.max_usage
    )

@router.get("", response_model=list[ApiKeyResponse])
async def list_api_keys(current_user: User = Depends(get_current_active_user)):
    """List all API keys for the authenticated user"""
    user_keys = []
    for key, data in api_keys_db.items():
        if data["user_id"] == current_user.id and data["is_active"]:
            user_keys.append(
                ApiKeyResponse(
                    key=key,
                    expires_at=data["expires_at"],
                    created_at=data["created_at"],
                    max_usage=data["max_usage"]
                )
            )
    return user_keys

@router.delete("/{key}")
async def revoke_api_key(
    key: str, 
    current_user: User = Depends(get_current_active_user)
):
    """Revoke an API key"""
    if key not in api_keys_db:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    
    if api_keys_db[key]["user_id"] != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to revoke this API key"
        )
    
    api_keys_db[key]["is_active"] = False
    
    return {"message": "API key revoked successfully"}
