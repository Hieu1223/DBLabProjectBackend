from fastapi import APIRouter, Header, HTTPException, Query,Body
from typing import Optional
from ..management.comments import *
from ..management.auth import authorize_comment, authorize_channel

router = APIRouter(prefix="/comments", tags=["Comments"])



@router.get("/{video_id}")
def list_comments(
    video_id: str,
    page: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100)
):
    try:
        return get_comments(video_id, page, page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/")
def create_comment_route(
    video_id: str = Body(...),
    user_id: str = Body(...),
    content: str = Body(...),
    auth_token: str = Body(...)
):

    if not authorize_channel(user_id, auth_token):
        raise HTTPException(status_code=403, detail="No auth_token")

    try:
        comment = create_comment(video_id, user_id, content)
        return {"message": "Comment created","result" : comment}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/{comment_id}")
def update_comment_route(
    comment_id: str,
    content: str = Body(...),
    auth_token: str = Body(...)
):

    if not authorize_comment(comment_id, auth_token):
        raise HTTPException(status_code=403, detail="No auth_token")

    try:
        comment = update_comment(comment_id, content)
        return {"message": "Comment updated","result":comment }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{comment_id}/like")
def like_comment_route(comment_id: str):
    try:
        like_comment(comment_id)
        return {"message": "Comment liked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{comment_id}/dislike")
def dislike_comment_route(comment_id: str):
    try:
        dislike_comment(comment_id)
        return {"message": "Comment disliked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/{comment_id}")
def delete_comment_route(
    comment_id: str,
    auth_token: str = Body(...,embed=True)
):
    if not authorize_comment(comment_id, auth_token):
        raise HTTPException(status_code=403, detail="No auth_token")

    try:
        delete_comment(comment_id)
        return {"message": "Comment deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
