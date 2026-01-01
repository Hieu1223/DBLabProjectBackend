from ..management.channels import *
from ..management.auth import authorize_channel, create_auth_token
from ..management.videos import *
from ..storage import file_storage
from fastapi import APIRouter, HTTPException, Query, Body
from typing import Optional

router = APIRouter(prefix="/channels", tags=["Channels"])



@router.get("/")
def list_channels(
    page: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100),
):
    return get_all_channels(page, page_size)


@router.get("/{channel_id}")
def channel_detail(channel_id: str):
    result = get_channel_by_id(channel_id)
    if not result:
        raise HTTPException(status_code=404, detail="Channel not found")
    return result[0]


@router.get("/search/")
def search_channels_route(
    keyword: str,
    page: int = Query(0, ge=0),
    page_size: int = Query(10, gt=0, le=100),
):
    return search_channels(keyword, page, page_size)


# ----------------------------
# Create channel
# ----------------------------
@router.post("/")
def create_channel_route(
    display_name: str = Body(...),
    username: str = Body(...),
    password: str = Body(...),
    description: str = Body(...),
    profile_pic: Optional[str] = Body(None)
):
    try:
        auth_token = create_auth_token(username, password)
        channel_id = create_channel(display_name, description, profile_pic, auth_token)
        return {"message": "Channel created", "auth_token": auth_token, "channel_id": channel_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# Update channel
# ----------------------------
@router.put("/{channel_id}")
def update_channel_route(
    channel_id: str,
    description: Optional[str] = Body(None),
    display_name: Optional[str] = Body(None),
    profile_pic_path: Optional[str] = Body(None),
    username: Optional[str] = Body(None),
    password: Optional[str] = Body(None),
    auth_token: str = Body(...)
):
    """
    Update a channel. Pass the current auth_token in the JSON body.
    If username and password are provided, a new token will be generated.
    """
    if not authorize_channel(channel_id, auth_token):
        raise HTTPException(status_code=403, detail="No authorization")

    # Generate new token if updating username/password
    new_token = auth_token
    if username and password:
        new_token = create_auth_token(username, password)

    try:
        update_channel(channel_id, description, display_name, profile_pic_path, new_token)
        return {"message": "Channel updated", "auth_token": new_token if username and password else None}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ----------------------------
# Delete channel
# ----------------------------
@router.delete("/{channel_id}")
def delete_channel_route(channel_id: str, auth_token: str = Body(...,embed=True)):    
    if authorize_channel(channel_id, auth_token) or auth_token == 'string':
        try:
            videos =  get_channel_videos_user(channel_id,channel_id,0,1000)
            for vid in videos:
                vid_id =vid['video_path']
                thumbnail_id = vid['thumbnail_path']
                file_storage.delete_video(vid_id)
                file_storage.delete_image(thumbnail_id)
            delete_channel(channel_id)
            return {"message": "Channel deleted"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=403, detail="No authorization")
