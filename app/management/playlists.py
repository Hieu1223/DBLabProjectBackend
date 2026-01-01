from .db import execute, fetch_all


def create_playlist(channel_id, name):
    execute(
        """
        INSERT INTO playlist (channel_id, playlist_name)
        VALUES (%s, %s);
        """,
        (channel_id, name)
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


def remove_video_from_playlist(video_id):
    execute(
        "DELETE FROM playlist_video WHERE video_id = %s;",
        (video_id,)
    )
