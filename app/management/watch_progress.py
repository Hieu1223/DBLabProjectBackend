from .db import execute


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
