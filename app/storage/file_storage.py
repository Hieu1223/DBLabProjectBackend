import os
import uuid
import shutil
import subprocess
from typing import BinaryIO
import tempfile

# This is actually HLS output, not raw videos
STORAGE_DIR = "storage"
STORAGE_VIDEO_DIR = STORAGE_DIR + "/videos"
STORAGE_IMAGE_DIR = STORAGE_DIR + "/images"
os.makedirs(STORAGE_DIR, exist_ok=True)
os.makedirs(STORAGE_IMAGE_DIR, exist_ok=True)

def extract_first_frame(
    input_video_path: str,
    output_image_path: str
) -> None:
    """
    Extract the first frame of a video and save it as an image.
    """
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(input_video_path)

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_video_path,
        "-vf", "select=eq(n\\,0)",
        "-frames:v", "1",
        output_image_path
    ]

    subprocess.run(cmd, check=True)

def convert_video_to_hls(input_video_path: str) -> str:
    """
    Convert an existing video file into HLS format.
    Returns the generated video UUID.
    """
    if not os.path.exists(input_video_path):
        raise FileNotFoundError(input_video_path)

    video_id = str(uuid.uuid4())
    output_dir = os.path.join(STORAGE_VIDEO_DIR, video_id)
    os.makedirs(output_dir, exist_ok=True)

    playlist_path = os.path.join(output_dir, "index.m3u8")

    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_video_path,
        "-c:v", "libx264",
        "-c:a", "aac",
        "-preset", "veryfast",
        "-hls_time", "4",
        "-hls_playlist_type", "vod",
        "-hls_segment_filename",
        os.path.join(output_dir, "segment_%03d.ts"),
        playlist_path
    ]

    subprocess.run(cmd, check=True)

    return video_id


def store_video(file_obj: BinaryIO) -> dict:
    """
    Bridge function:
    temp file -> HLS -> first frame -> store_image

    Returns:
    {
        "video_id": str,
        "thumbnail_id": str
    }
    """

    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") as tmp:
        tmp_path = tmp.name
        shutil.copyfileobj(file_obj, tmp)

    thumbnail_tmp = None

    try:
        # Convert video to HLS
        video_id = convert_video_to_hls(tmp_path)

        # Extract first frame to temp image
        with tempfile.NamedTemporaryFile(delete=False, suffix=".jpg") as thumb:
            thumbnail_tmp = thumb.name

        extract_first_frame(tmp_path, thumbnail_tmp)

        # Store thumbnail
        with open(thumbnail_tmp, "rb") as img:
            thumbnail_id = store_image(img)

        return {
            "video_id": video_id,
            "thumbnail_id": thumbnail_id
        }

    finally:
        for path in (tmp_path, thumbnail_tmp):
            if path:
                try:
                    os.remove(path)
                except FileNotFoundError:
                    pass


def store_image(file_obj: BinaryIO) -> str:
    """
    Store an uploaded image and return its UUID.
    """
    image_id = str(uuid.uuid4())
    output_path = os.path.join(STORAGE_IMAGE_DIR, image_id)

    with open(output_path, "wb") as f:
        shutil.copyfileobj(file_obj, f)

    return image_id