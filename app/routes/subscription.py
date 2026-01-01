from fastapi import APIRouter, HTTPException, Header, Body
from typing import Optional
from ..management.subscriptions import subscribe_channel, unsubscribe_channel
from ..management.auth import authorize_channel, authorize_subscription

router = APIRouter(prefix="/subscription", tags=["Subscriptions"])


@router.post("/")
def subscribe_route(
    channel_id: str = Body(..., embed=True),
    subscriber_id : str = Body(..., embed=True),
    auth_token: str = Body(...,embed=True)
):
    if not authorize_channel(subscriber_id,auth_token): 
        raise HTTPException(status_code=403, detail="Invalid auth token")

    try:
        subscribe_channel(channel_id, subscriber_id)
        return {"message": "Subscribed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.delete("/")
def unsubscribe_route(
    auth_token: str = Body(...,embed=True),
    channel_id: str = Body(..., embed=True),
    subscriber_id : str = Body(..., embed=True),
):
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="Invalid auth token")
    try:
        unsubscribe_channel(channel_id, subscriber_id)
        return {"message": "Unsubscribed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
