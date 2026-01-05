from fastapi import APIRouter, HTTPException, Body, Query, Header
from typing import Optional
from ..management.playlists import *
from ..management.auth import *

router = APIRouter(prefix="/playlists", tags=["Playlists"])

@router.post("/")
def create_playlist_route(
    channel_id: str = Body(...),
    name: str = Body(...),
    auth_token: str = Body(...)
):
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="No authorization")

    try:
        playlist = create_playlist(channel_id, name)
        return playlist
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

@router.get("/{channel_id}")
def get_playlist_route(
    channel_id: str,
    page: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100)
):
    try:
        return get_playlist_in_channel(channel_id,page_size,page)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/{playlist_id}/videos")
def add_video_to_playlist_route(
    playlist_id: str,
    video_id: str = Body(...),
    auth_token: str = Body(...)
):
    if not authorize_playlist(playlist_id,auth_token):
        raise HTTPException(status_code=403, detail="No authorization")
    try:
        add_video_to_playlist(playlist_id, video_id)
        return {"message": "Video added to playlist"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{playlist_id}/videos")
def get_videos_in_playlist_route(
    playlist_id: str,
    page: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100)
):
    try:
        return get_video_in_playlist(playlist_id, page, page_size)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{playlist_id}/{video_id}")
def remove_video_from_playlist_route(
    video_id: str,
    playlist_id:str,
    auth_token: str = Body(...,embed=True)
):
    if not authorize_playlist(playlist_id,auth_token):
        raise HTTPException(status_code=403, detail="No authorization")
    try:
        remove_video_from_playlist(video_id)
        return {"message": "Video removed from playlist"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/from_video/{video_id}/{channel_id}")
def list_playlist_from_video_and_user_route(
    video_id: str,
    channel_id: str
):
    try:
        return list_playlist_from_video_and_user(video_id, channel_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{playlist_id}")
def delete_playlist_route(
    playlist_id: str,
    auth_token: str = Body(...,embed=True)
):
    if not authorize_playlist(playlist_id,auth_token):
        raise HTTPException(status_code=403, detail="No authorization")
    try:
        delete_playlist(playlist_id)
        return {"message": "Playlist deleted"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

