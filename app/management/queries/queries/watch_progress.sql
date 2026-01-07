-- File: watch_progress.py
-- Query: upsert_watch_progress
INSERT INTO watch_progress (channel_id, video_id, last_position_second)
VALUES (%s, %s, %s) ON CONFLICT (channel_id, video_id) DO
UPDATE
SET last_position_second = EXCLUDED.last_position_second;
-- Query: get_watch_progress
SELECT video_id,
    last_position_second
FROM watch_progress
WHERE channel_id = %s;