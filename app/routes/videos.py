from fastapi import APIRouter, HTTPException, Body, Query,Form,UploadFile,File
from typing import Optional
from ..management.videos import *
from ..management.auth import *
from .auth import *
from ..storage import file_storage

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


@router.get("/liked")
def liked_videos_route(
    viewer_id: str = Query(...),
    auth_token: str = Query(...),
    page: int = Query(0, ge=0),
    page_size: int = Query(20, ge=1, le=50)
):
    """
    Get videos liked by a user (viewer_id) with pagination.
    """
    # Authorization check
    if not authorize_channel(viewer_id, auth_token):
        raise HTTPException(status_code=403, detail="Invalid auth token")

    try:
        videos = get_liked_videos(viewer_id, page, page_size)
        return {
            "page": page,
            "page_size": page_size,
            "total": len(videos),
            "videos": videos
        }
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


@router.put("/channel/{channel_id}/{video_id}")
async def update_video_route(
    video_id: str,
    channel_id :str,
    auth_token: str = Form(...),

    title: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    privacy: Optional[str] = Form(None),

    thumbnail_file: Optional[UploadFile] = File(None)
):
    # ----------------------------
    # Authorization
    # ----------------------------
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="No authorization")
    try:
        # ----------------------------
        # Handle thumbnail upload
        # ----------------------------
        thumbnail_path = None
        if thumbnail_file:
            stored = file_storage.store_image(thumbnail_file.file)
            thumbnail_path = f"files/images/{stored}"
        # ----------------------------
        # Update DB
        # ----------------------------
        update_video(
            video_id=video_id,
            title=title,
            description=description,
            thumbnail_path=thumbnail_path,
            privacy=privacy
        )

        # ----------------------------
        # Fetch updated video
        # ----------------------------
        video = fetch_one(
            "SELECT * FROM video WHERE video_id = %s",
            (video_id,)
        )

        return {
            "message": "Video updated",
            "video": video
        }

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
async def create_video_route(
    channel_id: str = Form(...),
    auth_token: str = Form(...),
    title: str = Form(...),
    description: str = Form(...),
    video_file: UploadFile = File(...)
):
    # ----------------------------
    # Authorization
    # ----------------------------
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="No authorization")

    try:
        # ----------------------------
        # Store video + auto-generate paths
        # ----------------------------
        stored = file_storage.store_video(video_file.file)
        video_path =f"files/videos/{stored["video_id"]}/index.m3u8"
        thumbnail_path = f"files/images/{stored["thumbnail_id"]}"

        # ----------------------------
        # DB insert (UNCHANGED)
        # ----------------------------
        video = create_video(
            channel_id,
            title,
            description,
            video_path,
            thumbnail_path
        )

        return {
            "message": "Video created",
            "video": video
        }

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
    video = get_video(channel_id,video_id)
    if not video:
        raise HTTPException(status_code=404, detail="Video not found")

    if not authorize_video(video_id, auth_token):
        raise HTTPException(status_code=403, detail="Not your video")
    try:
        file_storage.delete_video(video["video_path"])
        file_storage.delete_image(video["thumbnail_path"])
        delete_video(video_id)
        return {"message": "Video deleted",'extra': video["thumbnail_path"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

