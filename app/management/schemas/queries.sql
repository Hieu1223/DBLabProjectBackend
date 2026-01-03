-- Exported SQL queries from app/management (Python files)
-- File: auth.py
-- Query: authorize_channel
SELECT 1 FROM channel WHERE channel_id = %s AND auth_token = %s LIMIT 1;

-- Query: authorize_video
SELECT 1
FROM channel
JOIN video ON video.channel_id = channel.channel_id
WHERE channel.auth_token = %s AND video.video_id = %s
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
WHERE channel.auth_token = %s AND comment.comment_id = %s
LIMIT 1;

-- Query: authorize_subscription
SELECT 1
FROM channel
JOIN subscription ON subscription.subscriber_id = channel.channel_id
WHERE channel.auth_token = %s AND subscription.subscriber_id = %s
LIMIT 1;

-- Query: get_id_from_token
SELECT channel_id
FROM channel
WHERE auth_token = %s;

-- File: channels.py
-- Query: get_all_channels
SELECT channel_id,display_name FROM channel ORDER BY subscriber_count DESC LIMIT %s OFFSET %s;

-- Query: get_channel_by_id
SELECT * FROM channel WHERE channel_id = %s;

-- Query: search_channels
SELECT channel_id,display_name,profile_pic_path,subscriber_count FROM channel
WHERE LOWER(display_name) LIKE %s
ORDER BY subscriber_count DESC
LIMIT %s OFFSET %s;

-- Query: create_channel
INSERT INTO channel (display_name, description, profile_pic_path, auth_token)
VALUES (%s, %s, %s, %s)
RETURNING channel_id;

-- Query: update_channel (dynamic)
UPDATE channel
SET {comma-separated fields}
WHERE channel_id = %s;

-- Query: delete_channel
DELETE FROM channel WHERE channel_id = %s;

-- File: comments.py
-- Query: get_comments
SELECT *
FROM comment
WHERE video_id = %s
ORDER BY comment_time DESC
LIMIT %s OFFSET %s;

-- Query: create_comment
INSERT INTO comment (video_id, channel_id, content)
VALUES (%s, %s, %s)
RETURNING *;

-- Query: update_comment
UPDATE comment
SET content = %s,
comment_time = NOW()
WHERE comment_id = %s
RETURNING *;

-- Query: like_comment
UPDATE comment
SET like_count = COALESCE(like_count, 0) + 1
WHERE comment_id = %s;

-- Query: dislike_comment
UPDATE comment
SET dislike_count = COALESCE(dislike_count, 0) + 1
WHERE comment_id = %s;

-- Query: delete_comment
DELETE FROM comment WHERE comment_id = %s;

-- File: playlists.py
-- Query: get_playlist_in_channel
select * from playlist
where channel_id = %s
limit %s offset %s;

-- Query: create_playlist
INSERT INTO playlist (channel_id, playlist_name)
VALUES (%s, %s)
RETURNING *;

-- Query: add_video_to_playlist
INSERT INTO playlist_video (playlist_id, video_id)
VALUES (%s, %s);

-- Query: delete_playlist
DELETE FROM playlist WHERE playlist_id = %s;

-- Query: remove_video_from_playlist
DELETE FROM playlist_video WHERE video_id = %s;

-- Query: get_video_in_playlist
select video.video_id,title, thumbnail_path from playlist
natural join playlist_video
join video on video.video_id = playlist_video.video_id
WHERE playlist.playlist_id = %s
LIMIT %s OFFSET %s;

-- File: reactions.py
-- Query: get video reaction
SELECT reaction_type FROM video_reactions WHERE channel_id = %s AND video_id = %s;

-- Query: decrement video like count
UPDATE video SET like_count = GREATEST(COALESCE(like_count,0) - 1, 0) WHERE video_id = %s;

-- Query: decrement video dislike count
UPDATE video SET dislike_count = GREATEST(COALESCE(dislike_count,0) - 1, 0) WHERE video_id = %s;

-- Query: update video reaction
UPDATE video_reactions SET reaction_type = %s WHERE channel_id = %s AND video_id = %s;

-- Query: insert video reaction
INSERT INTO video_reactions (channel_id, video_id, reaction_type) VALUES (%s, %s, %s);

-- Query: increment video like count
UPDATE video SET like_count = COALESCE(like_count,0) + 1 WHERE video_id = %s;

-- Query: increment video dislike count
UPDATE video SET dislike_count = COALESCE(dislike_count,0) + 1 WHERE video_id = %s;

-- Query: get comment reaction
SELECT reaction_type FROM comment_reactions WHERE channel_id = %s AND comment_id = %s;

-- Query: decrement comment like count
UPDATE comment SET like_count = GREATEST(COALESCE(like_count,0) - 1, 0) WHERE comment_id = %s;

-- Query: decrement comment dislike count
UPDATE comment SET dislike_count = GREATEST(COALESCE(dislike_count,0) - 1, 0) WHERE comment_id = %s;

-- Query: update comment reaction
UPDATE comment_reactions SET reaction_type = %s WHERE channel_id = %s AND comment_id = %s;

-- Query: insert comment reaction
INSERT INTO comment_reactions (channel_id, comment_id, reaction_type) VALUES (%s, %s, %s);

-- Query: increment comment like count
UPDATE comment SET like_count = COALESCE(like_count,0) + 1 WHERE comment_id = %s;

-- Query: increment comment dislike count
UPDATE comment SET dislike_count = COALESCE(dislike_count,0) + 1 WHERE comment_id = %s;

-- File: subscriptions.py
-- Query: subscribe_channel (insert)
INSERT INTO "subscription" (channel_id, subscriber_id)
VALUES (%s, %s);

-- Query: increment subscriber count
UPDATE channel
SET subscriber_count = COALESCE(subscriber_count, 0) + 1
WHERE channel_id = %s;

-- Query: unsubscribe_channel (delete)
DELETE FROM "subscription"
WHERE channel_id = %s AND subscriber_id = %s;

-- Query: decrement subscriber count
UPDATE channel
SET subscriber_count = COALESCE(subscriber_count, 0) - 1
WHERE channel_id = %s;

-- Query: get_subscribed_channels
SELECT c.*
FROM "subscription" s
JOIN channel c ON c.channel_id = s.channel_id
WHERE s.subscriber_id = %s
ORDER BY c.subscriber_count DESC
LIMIT %s OFFSET %s;

-- Query: check_subscription
SELECT 1
FROM "subscription" s
WHERE s.subscriber_id = %s and s.channel_id = %s;

-- File: videos.py
-- Query: get_accessible_videos_user
SELECT video_id,channel_id,title,description,upload_time,thumbnail_path,views_count
FROM video
WHERE video.channel_id = %s or video.privacy = 'public'
ORDER BY video.upload_time DESC
LIMIT %s OFFSET %s;

-- Query: get_accessible_videos_guest
SELECT video_id,channel_id,title,upload_time,thumbnail_path,views_count
FROM video
WHERE video.privacy = 'public'
ORDER BY video.upload_time DESC
LIMIT %s OFFSET %s;

-- Query: get_channel_videos_guest
SELECT video_id,channel_id,title,upload_time,thumbnail_path,views_count,null as last_position_second
FROM video
WHERE video.channel_id = %s and video.privacy = 'public'
LIMIT %s OFFSET %s;

-- Query: get_channel_videos_user
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

-- Query: search_videos
SELECT video_id,channel_id,title,upload_time,thumbnail_path,views_count
FROM video
WHERE LOWER(title) LIKE %s
ORDER BY video.upload_time DESC
LIMIT %s OFFSET %s;

-- Query: create_video
INSERT INTO video (channel_id, title, description, video_path, thumbnail_path)
VALUES (%s, %s, %s, %s, %s)
RETURNING *;

-- Query: update_video (dynamic)
UPDATE video
SET {comma-separated fields}
WHERE video_id = %s;

-- Query: get_video (viewer exists)
SELECT video.*,v_channel.display_name, v_channel.profile_pic_path, watch_progress.last_position_second
FROM video
JOIN v_channel ON v_channel.channel_id = video.channel_id
LEFT JOIN watch_progress
ON watch_progress.video_id = video.video_id
AND watch_progress.channel_id = %s
WHERE video.video_id = %s
AND (video.privacy = 'public' OR video.channel_id = %s);

-- Query: get_video (guest)
SELECT video.*, NULL AS last_position_second
FROM video
JOIN v_channel ON v_channel.channel_id = video.channel_id
WHERE video.video_id = %s
AND (video.privacy = 'public' OR video.privacy = 'limited');

-- Query: get_liked_videos
SELECT v.*, c.profile_pic_path,c.display_name
FROM video_reactions vr
JOIN video v ON vr.video_id = v.video_id
JOIN channel c ON c.channel_id = v.channel_id
WHERE vr.channel_id = %s
AND vr.reaction_type = 'like'
LIMIT %s OFFSET %s;

-- Query: increase_view
UPDATE video
SET views_count = COALESCE(views_count, 0) + 1
WHERE video_id = %s;

-- Query: delete_video
DELETE FROM video WHERE video_id = %s;

-- File: watch_progress.py
-- Query: upsert_watch_progress
INSERT INTO watch_progress (channel_id, video_id, last_position_second)
VALUES (%s, %s, %s)
ON CONFLICT (channel_id, video_id)
DO UPDATE SET last_position_second = EXCLUDED.last_position_second;

-- Query: get_watch_progress
SELECT
video_id,
last_position_second
FROM watch_progress
WHERE channel_id = %s;