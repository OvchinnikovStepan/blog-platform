import httpx
from fastapi import Request, HTTPException, Depends

USERS_SERVICE_URL = "http://users-service:8000"   # имя контейнера

async def verify_token(request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    async with httpx.AsyncClient() as client:
        resp = await client.get(
            f"{USERS_SERVICE_URL}/users/me",
            headers={"Authorization": auth_header}
        )

    if resp.status_code != 200:
        raise HTTPException(status_code=401, detail="Invalid token")

    return resp.json()  # данные пользователя из users-service
