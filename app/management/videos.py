from .db import *


def get_accessible_videos_user(viewer_channel_id: str, page: int = 0, page_size: int = 10):
    query = """
    SELECT video_id,channel_id,title,description,upload_time,thumbnail_path,views_count
    FROM video
    WHERE video.channel_id = %s or video.privacy = 'public'
    ORDER BY video.upload_time DESC
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (viewer_channel_id, page_size, page * page_size))



def get_accessible_videos_guest(page: int = 0, page_size: int = 10):
    query = """
    SELECT video_id,channel_id,title,upload_time,thumbnail_path,views_count
    FROM video
    WHERE video.privacy = 'public'
    ORDER BY video.upload_time DESC
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (page_size, page * page_size))


def get_channel_videos_guest(channel_id, page: int = 0, page_size: int = 10):
    query = """
    SELECT video_id,channel_id,title,upload_time,thumbnail_path,views_count,null as last_position_second
    FROM video
    WHERE video.channel_id = %s and video.privacy = 'public'
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (channel_id, page_size, page * page_size))


def get_channel_videos_user(viewer_id, owner_id, page: int = 0, page_size: int = 10):
    query = """
    SELECT video_id,video.channel_id,title,upload_time,thumbnail_path,views_count,video_path
    FROM video
    WHERE video.channel_id = %s
      AND (
          video.privacy = 'public'
          OR video.privacy = 'limited'
          OR video.channel_id = %s
      )
    ORDER BY video.upload_time DESC
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (owner_id,viewer_id, page_size, page * page_size))


def search_videos(keyword, page: int = 0, page_size: int = 10):
    query = """
    SELECT video_id,channel_id,title,upload_time,thumbnail_path,views_count
    FROM video
    WHERE LOWER(title) LIKE %s
    ORDER BY video.upload_time DESC
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (f"%{keyword.lower()}%", page_size, page * page_size))



def create_video(channel_id, title, description, path, thumbnail_path):
    """
    Create a new video and return the inserted row.
    """
    query = """
    INSERT INTO video (channel_id, title, description, video_path, thumbnail_path)
    VALUES (%s, %s, %s, %s, %s)
    RETURNING *;
    """
    result = fetch_one(query, (channel_id, title, description, path, thumbnail_path))
    return result


def update_video(
    video_id,
    title=None,
    description=None,
    thumbnail_path=None,
    privacy=None
):
    fields = []
    values = []

    if title is not None:
        fields.append("title = %s")
        values.append(title)

    if description is not None:
        fields.append("description = %s")
        values.append(description)

    if thumbnail_path is not None:
        fields.append("thumbnail_path = %s")
        values.append(thumbnail_path)

    if privacy is not None:
        fields.append("privacy = %s")
        values.append(privacy)

    if not fields:
        return

    values.append(video_id)

    query = f"""
        UPDATE video
        SET {", ".join(fields)}
        WHERE video_id = %s;
    """

    execute(query, tuple(values))

def get_video(viewer_id: str, video_id: str):
    if viewer_id:
        # Viewer exists → join watch_progress
        query = """
        SELECT video.*,v_channel.display_name, v_channel.profile_pic_path, watch_progress.last_position_second
        FROM video
        JOIN v_channel ON v_channel.channel_id = video.channel_id
        LEFT JOIN watch_progress
            ON watch_progress.video_id = video.video_id
           AND watch_progress.channel_id = %s
        WHERE video.video_id = %s
          AND (video.privacy = 'public' OR video.channel_id = %s);
        """
        return fetch_one(query, (viewer_id, video_id, viewer_id))
    else:
        # No viewer → only public or limited videos, last_position_second = NULL
        query = """
        SELECT video.*, NULL AS last_position_second
        FROM video
        JOIN v_channel ON v_channel.channel_id = video.channel_id
        WHERE video.video_id = %s
          AND (video.privacy = 'public' OR video.privacy = 'limited');
        """
        return fetch_one(query, (video_id,))

def get_liked_videos(viewer_id: str, page: int = 0, page_size: int = 20):
    """
    Returns a paginated list of videos that the user (viewer_id) has liked.
    """
    offset = page * page_size

    query = """
        SELECT v.*, c.profile_pic_path,c.display_name
        FROM video_reactions vr
        JOIN video v ON vr.video_id = v.video_id
        JOIN channel c ON c.channel_id = v.channel_id
        WHERE vr.channel_id = %s
          AND vr.reaction_type = 'like'
        LIMIT %s OFFSET %s;
    """

    return fetch_all(query, (viewer_id, page_size, offset))

def increase_view(video_id):
    execute(
        """
        UPDATE video
        SET views_count = COALESCE(views_count, 0) + 1
        WHERE video_id = %s;
        """,
        (video_id,)
    )

def delete_video(video_id):
    execute("DELETE FROM video WHERE video_id = %s;", (video_id,))
