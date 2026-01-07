from .db import *


def get_playlist_in_channel(channel_id,page_size, page):
    query = """
    select * from playlist
    where channel_id = %s
    limit %s offset %s;
    """
    return fetch_all(query, (channel_id,page_size, page_size* page))


def create_playlist(channel_id, name):
    return execute(
        """
        INSERT INTO playlist (channel_id, playlist_name)
        VALUES (%s, %s)
        RETURNING *;
        """,
        (channel_id, name),
        fetch_one=True,
    )


def add_video_to_playlist(playlist_id, video_id):
    execute(
        """
        INSERT INTO playlist_video (playlist_id, video_id)
        VALUES (%s, %s);
        """,
        (playlist_id, video_id)
    )


def delete_playlist(playlist_id):
    execute(
        "DELETE FROM playlist WHERE playlist_id = %s;",
        (playlist_id,)
    )


def list_playlist_from_video_and_user(video_id, channel_id):
    query = """
    select playlist.playlist_id, playlist_name from playlist
    natural join playlist_video
    where playlist_video.video_id = %s and playlist.channel_id = %s;
    """
    return fetch_all(
        query,
        (video_id, channel_id)
    )

def remove_video_from_playlist(video_id):
    execute(
        "DELETE FROM playlist_video WHERE video_id = %s;",
        (video_id,)
    )

def get_video_in_playlist(playlist_id: str, page: int = 0, page_size: int = 10):
    query = """
    select video.video_id,title, thumbnail_path from playlist
    natural join playlist_video
    join video on video.video_id = playlist_video.video_id
    WHERE playlist.playlist_id = %s
    LIMIT %s OFFSET %s;
    """
    return fetch_all(
        query,
        (playlist_id, page_size, page * page_size)
    )
