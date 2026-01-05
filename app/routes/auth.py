from fastapi import APIRouter, HTTPException, Header, Query,Body
from fastapi import APIRouter, Header, HTTPException
from fastapi.security import APIKeyHeader
from typing import Optional
from ..management.auth import get_id_from_token,create_auth_token


auth_scheme = APIKeyHeader(name="Authorization", auto_error=True)
router = APIRouter(prefix="/auth", tags=["Auth"])




@router.get("/token")
def get_auth_token_route(username: str, password: str):
    token = create_auth_token(username, password)
    return {"auth_token": token}

@router.get("/id")
def get_id_from_token_route(token):
    return {"channel_id": get_id_from_token(token)}
