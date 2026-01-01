from .db import *


def get_accessible_videos_user(viewer_channel_id: str, page: int = 0, page_size: int = 10):
    query = """
    SELECT video_id
    FROM video
    ORDER BY video.upload_time DESC
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (viewer_channel_id, viewer_channel_id, page_size, page * page_size))



def get_accessible_videos_guest(page: int = 0, page_size: int = 10):
    query = """
    SELECT video_id,title
    FROM video
    ORDER BY video.upload_time DESC
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (page_size, page * page_size))


def get_channel_videos_guest(channel_id, page: int = 0, page_size: int = 10):
    query = """
    SELECT video_id
    FROM video
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (channel_id, page_size, page * page_size))


def get_channel_videos_user(viewer_id, owner_id, page: int = 0, page_size: int = 10):
    query = """
    SELECT *
    FROM video
    JOIN v_channel ON v_channel.channel_id = video.channel_id
    WHERE video.channel_id = %s
      AND (
          video.privacy = 'public'
          OR video.privacy = 'limited'
          OR video.channel_id = %s
      )
    ORDER BY video.upload_time DESC
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (viewer_id, owner_id, page_size, page * page_size))


def search_videos(keyword, page: int = 0, page_size: int = 10):
    query = """
    SELECT video_id,title
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


def get_video(viewer_id: str, video_id: str):
    if viewer_id:
        # Viewer exists → join watch_progress
        query = """
        SELECT video.*, watch_progress.last_position_second
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


def like_video(video_id):
    execute(
        """
        UPDATE video
        SET like_count = COALESCE(like_count, 0) + 1
        WHERE video_id = %s;
        """,
        (video_id,)
    )


def dislike_video(video_id):
    execute(
        """
        UPDATE video
        SET dislike_count = COALESCE(dislike_count, 0) + 1
        WHERE video_id = %s;
        """,
        (video_id,)
    )

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
