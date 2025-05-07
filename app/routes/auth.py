from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta, datetime
from app.models import UserCreate, User, Token
from app.auth import (
    ACCESS_TOKEN_EXPIRE_MINUTES, 
    authenticate_user, 
    create_access_token, 
    get_password_hash,
    get_current_active_user,
    users_db
)

router = APIRouter(tags=["authentication"])

@router.post("/signup", response_model=User)
async def create_user(user: UserCreate):
    if user.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    hashed_password = get_password_hash(user.password)
    db_user = {
        "id": user.username,  # Using username as ID for simplicity
        "username": user.username,
        "email": user.email,
        "hashed_password": hashed_password,
        "disabled": False
    }
    users_db[user.username] = db_user
    
    return User(
        id=db_user["id"],
        username=db_user["username"],
        email=db_user["email"],
        disabled=db_user["disabled"],
        created_at=db_user.get("created_at", datetime.utcnow())
    )

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
