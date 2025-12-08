from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import httpx
from fastapi import Request, HTTPException, Depends, status
from config.config import settings
from jose import JWTError, jwt

USERS_SERVICE_URL = "http://users-service:8000"

security = HTTPBearer()


def decode_token(token: str) -> dict:
    """Декодирование JWT токена"""
    try:
        payload = jwt.decode(token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM])
        return payload
    except JWTError:
        return None

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    if not credentials or not credentials.credentials:
                raise HTTPException(status_code=401, detail="Missing Authorization header")
    else:
            token = credentials.credentials
            payload = decode_token(token)
            
            if payload is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            user_id: int = payload.get("user_id")
            if user_id is None:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Could not validate credentials",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            response={"id":user_id}
            return response

