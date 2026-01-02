from .db import *


def upsert_watch_progress(channel_id, video_id, seconds):
    execute(
        """
        INSERT INTO watch_progress (channel_id, video_id, last_position_second)
        VALUES (%s, %s, %s)
        ON CONFLICT (channel_id, video_id)
        DO UPDATE SET last_position_second = EXCLUDED.last_position_second;
        """,
        (channel_id, video_id, seconds)
    )

def get_watch_progress(channel_id: str):
    return fetch_all(
        """
        SELECT
            video_id,
            last_position_second
        FROM watch_progress
        WHERE channel_id = %s;
        """,
        (channel_id,)
    )
