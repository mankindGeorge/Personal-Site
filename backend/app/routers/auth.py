from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel
from datetime import datetime, timedelta
import hashlib
import os

from app.config import get_settings

router = APIRouter(prefix="/api/auth", tags=["认证"])

settings = get_settings()


class LoginRequest(BaseModel):
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


def create_token(password: str) -> str:
    timestamp = str(int(datetime.now().timestamp()))
    data = f"{password}:{timestamp}:{settings.SECRET_KEY}"
    return hashlib.sha256(data.encode()).hexdigest()[:32]


@router.post("/login", response_model=TokenResponse)
def login(request: LoginRequest):
    if request.password != settings.ADMIN_PASSWORD:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="密码错误"
        )
    
    token = create_token(request.password)
    return TokenResponse(access_token=token)
