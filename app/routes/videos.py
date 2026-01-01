from fastapi import APIRouter, HTTPException, Body, Query
from typing import Optional
from ..management.videos import *
from ..management.auth import authorize_channel
from .auth import *

router = APIRouter(prefix="/video", tags=["Videos"])


@router.post("/accessible")
def accessible_videos_route(
    viewer_id: Optional[str] = Body(None, embed=True),
    page: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100)
):
    try:
        if viewer_id:
            return get_accessible_videos_user(viewer_id, page, page_size)
        else:
            return get_accessible_videos_guest(page, page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))





@router.post("/channel/{channel_id}")
def channel_videos_user_route(
    channel_id: str,
    auth_token: Optional[str] = Body(None, embed=True),
    page: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100)
):
    if auth_token is None:
        try:
            return get_channel_videos_guest(channel_id, page, page_size)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        try:
            id = get_id_from_token(auth_token)
            return get_channel_videos_user(id, channel_id, page, page_size)
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

@router.post("/aggregate/{video_id}")
def get_video_route(
    video_id: str,
    viewer_id: Optional[str] = Body(None, embed=True)
):
    video = get_video(viewer_id,video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found or is private")
    return video


@router.get("/search")
def search_videos_route(
    keyword: str,
    page: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100)
):
    try:
        return search_videos(keyword, page, page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# Create a new video
# ----------------------------
@router.post("/")
def create_video_route(
    channel_id: str = Body(..., embed=True),
    auth_token: str = Body(..., embed=True),
    title: str = Body(...),
    description: str = Body(...),
    path: str = Body(...),
    thumbnail_path: str = Body(...)
):
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="No authorization")
    try:
        video = create_video(channel_id, title, description, path,thumbnail_path)
        return {"message": "Video created","video": video}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# Like / Dislike / Delete video
# ----------------------------
@router.post("/{video_id}/like")
def like_video_route(video_id: str):
    try:
        like_video(video_id)
        return {"message": "Video liked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{video_id}/dislike")
def dislike_video_route(video_id: str):
    try:
        dislike_video(video_id)
        return {"message": "Video disliked"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{video_id}/view")
def increase_view_route(video_id: str):
    try:
        increase_view(video_id)
        return {"message": "Video viewed"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{video_id}")
def delete_video_route(video_id: str, channel_id: str = Body(..., embed=True), auth_token: str = Body(..., embed=True)):
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="No authorization")
    try:
        delete_video(video_id)
        return {"message": "Video deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

