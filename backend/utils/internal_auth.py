from fastapi import Header, HTTPException, status
import os

INTERNAL_TOKENS = {
    os.getenv("INTERNAL_MODERATION_TOKEN"):"moderation",
    os.getenv("INTERNAL_PREVIEW_TOKEN"): "preview",
    os.getenv("INTERNAL_PUBLISH_TOKEN"): "publish",
    os.getenv("INTERNAL_DLQ_TOKEN"): "dlq"}

def verify_internal_token(authorization: str = Header(...)):

    if not authorization.startswith("Token "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)

    token = authorization.removeprefix("Token ").strip()

    if token not in INTERNAL_TOKENS.keys:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)

    return token
