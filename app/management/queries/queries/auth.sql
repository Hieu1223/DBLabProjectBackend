-- File: auth.py
-- Query: authorize_channel
SELECT 1
FROM channel
WHERE channel_id = %s
    AND auth_token = %s
LIMIT 1;
-- Query: authorize_video
SELECT 1
FROM channel
    JOIN video ON video.channel_id = channel.channel_id
WHERE channel.auth_token = %s
    AND video.video_id = %s
LIMIT 1;
-- Query: authorize_playlist
SELECT 1
FROM playlist p
    JOIN channel c ON c.channel_id = p.channel_id
WHERE c.auth_token = %s
    AND p.playlist_id = %s
LIMIT 1;
-- Query: authorize_comment
SELECT 1
FROM channel
    JOIN comment ON comment.channel_id = channel.channel_id
WHERE channel.auth_token = %s
    AND comment.comment_id = %s
LIMIT 1;
-- Query: authorize_subscription
SELECT 1
FROM channel
    JOIN subscription ON subscription.subscriber_id = channel.channel_id
WHERE channel.auth_token = %s
    AND subscription.subscriber_id = %s
LIMIT 1;
-- Query: get_id_from_token
SELECT channel_id
FROM channel
WHERE auth_token = %s;