from fastapi import APIRouter, HTTPException,Query, Header, Body
from typing import Optional
from ..management.subscriptions import *
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

@router.post("/list")
def list_subscriptions_route(
    subscriber_id: str = Body(..., embed=True),
    auth_token: str = Body(..., embed=True),
    page: int = Query(0, ge=0),
    page_size: int = Query(10, ge=1, le=50),
):
    if not authorize_channel(subscriber_id, auth_token):
        raise HTTPException(status_code=403, detail="Invalid auth token")

    try:
        channels = get_subscribed_channels(
            subscriber_id=subscriber_id,
            page=page,
            page_size=page_size
        )
        return channels
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@router.get("/status")
async def get_subscription_status(
    subscriber_id: str = Query(...),
    channel_id: str = Query(...)
):
    try:
        result = check_subscription(subscriber_id, channel_id)
        
        return {"is_subscribed": len(result) > 0}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/")
def unsubscribe_route(
    auth_token: str = Body(...,embed=True),
    channel_id: str = Body(..., embed=True),
    subscriber_id : str = Body(..., embed=True),
):
    if not authorize_channel(subscriber_id, auth_token):
        raise HTTPException(status_code=403, detail="Invalid auth token")
    try:
        unsubscribe_channel(channel_id, subscriber_id)
        return {"message": "Unsubscribed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
