from fastapi import APIRouter, HTTPException, Header, Query,Body
from fastapi import APIRouter, Header, HTTPException
from fastapi.security import APIKeyHeader
from typing import Optional
from ..management.auth import get_id_from_token,create_auth_token


auth_scheme = APIKeyHeader(name="Authorization", auto_error=True)
router = APIRouter(prefix="/auth", tags=["Auth"])

# Helper to validate token
def get_auth_token(authorization: Optional[str] = Header(None)) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    # Expecting "Bearer <token>"
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    return parts[1]


@router.get("/token")
def get_auth_token_route(username: str, password: str):
    # Generate or return existing auth token
    token = create_auth_token(username, password)
    return {"auth_token": token}

@router.get("/id")
def get_id_from_token_route(token):
    return {"channel_id": get_id_from_token(token)}
