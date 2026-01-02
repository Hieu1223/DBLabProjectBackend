from fastapi import APIRouter, HTTPException, Body, Query
from typing import Literal, Optional
from ..management.auth import authorize_channel
from ..management.reactions import *

router = APIRouter(prefix="/reaction", tags=["Reactions"])

ReactionType = Literal["like", "dislike", "none"]
TargetType = Literal["video", "comment"]

@router.post("/")
def react_route(
    channel_id: str = Body(..., embed=True),
    auth_token: str = Body(..., embed=True),
    target_type: TargetType = Body(..., embed=True),
    target_id: str = Body(..., embed=True),
    reaction: ReactionType = Body(..., embed=True)
):
    """
    React to a video or comment.
    reaction: "like", "dislike", or None (to unlike/undislike)
    target_type: "video" or "comment"
    target_id: id of video or comment
    """
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="Invalid auth token")

    try:
        if target_type == "video":
            set_video_reaction(channel_id, target_id, reaction)
        elif target_type == "comment":
            set_comment_reaction(channel_id, target_id, reaction)
        else:
            raise HTTPException(status_code=400, detail="Invalid target_type")

        action = reaction if reaction else "removed"
        return {"message": f"{target_type.capitalize()} reaction {action}"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/")
def get_reaction_route(
    channel_id: str = Query(...),
    target_type: TargetType = Query(...),
    target_id: str = Query(...)
):
    """
    Get the current reaction of a user for a video or comment
    """
    try:
        if target_type == "video":
            reaction = get_video_reaction(channel_id, target_id)
        elif target_type == "comment":
            reaction = get_comment_reaction(channel_id, target_id)
        else:
            raise HTTPException(status_code=400, detail="Invalid target_type")

        return {"reaction": reaction}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
