from fastapi import APIRouter, HTTPException, Body
from ..management.auth import authorize_channel
from ..management.watch_progress import get_watch_progress, upsert_watch_progress

router = APIRouter(prefix="/history", tags=["History"])


# ----------------------------
# GET HISTORY
# ----------------------------
@router.post("/")
def get_watch_history(
    channel_id: str = Body(..., embed=True),
    auth_token: str = Body(..., embed=True),
):
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="Invalid auth token")

    try:
        return get_watch_progress(channel_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# UPDATE WATCH PROGRESS
# ----------------------------
@router.put("/")
def update_watch_history(
    channel_id: str = Body(..., embed=True),
    video_id: str = Body(..., embed=True),
    seconds: float = Body(..., embed=True),
    auth_token: str = Body(..., embed=True),
):
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="Invalid auth token")

    try:
        upsert_watch_progress(channel_id, video_id, seconds)
        return {"message": "Watch progress updated"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
