from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import httpx
from fastapi import Request, HTTPException, Depends

USERS_SERVICE_URL = "http://users-service:8000"

security = HTTPBearer()

async def verify_token(
    request: Request,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        if not credentials or not credentials.credentials:
            raise HTTPException(status_code=401, detail="Missing Authorization header")
        auth_header = f"Bearer {credentials.credentials}"

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{USERS_SERVICE_URL}/users/me",
            headers={"Authorization": auth_header}
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")

    return resp.json()
