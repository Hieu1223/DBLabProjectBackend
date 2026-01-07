-- File: videos.py
-- Query: get_accessible_videos_user
SELECT video_id,
    channel_id,
    title,
    description,
    upload_time,
    thumbnail_path,
    views_count
FROM video
WHERE video.channel_id = %s
    or video.privacy = 'public'
ORDER BY video.upload_time DESC
LIMIT %s OFFSET %s;
-- Query: get_accessible_videos_guest
SELECT video_id,
    channel_id,
    title,
    upload_time,
    thumbnail_path,
    views_count
FROM video
WHERE video.privacy = 'public'
ORDER BY video.upload_time DESC
LIMIT %s OFFSET %s;
-- Query: get_channel_videos_guest
SELECT video_id,
    channel_id,
    title,
    upload_time,
    thumbnail_path,
    views_count,
    null as last_position_second
FROM video
WHERE video.channel_id = %s
    and video.privacy = 'public'
LIMIT %s OFFSET %s;
-- Query: get_channel_videos_user
SELECT video_id,
    video.channel_id,
    title,
    upload_time,
    thumbnail_path,
    views_count,
    video_path,
    last_position_second
FROM video
    JOIN watch_progress on watch_progress.video_id = video.video_id,
    watch_progress.channel_id = %s
WHERE video.channel_id = %s
    AND (
        video.privacy = 'public'
        OR (
            video.privacy = 'limited'
            AND video.channel_id = %s
        )
    )
ORDER BY video.upload_time DESC
LIMIT %s OFFSET %s;
-- Query: search_videos
SELECT video_id,
    channel_id,
    title,
    upload_time,
    thumbnail_path,
    views_count
FROM video
WHERE LOWER(title) LIKE %s
ORDER BY video.upload_time DESC
LIMIT %s OFFSET %s;
-- Query: create_video
INSERT INTO video (
        channel_id,
        title,
        description,
        video_path,
        thumbnail_path
    )
VALUES (%s, %s, %s, %s, %s)
RETURNING *;
-- Query: update_video (dynamic)
UPDATE video
SET { comma - separated fields }
WHERE video_id = %s;
-- Query: get_video (viewer exists)
SELECT video.*,
    v_channel.display_name,
    v_channel.profile_pic_path,
    watch_progress.last_position_second
FROM video
    JOIN v_channel ON v_channel.channel_id = video.channel_id
    LEFT JOIN watch_progress ON watch_progress.video_id = video.video_id
    AND watch_progress.channel_id = %s
WHERE video.video_id = %s
    AND (
        video.privacy = 'public'
        OR video.channel_id = %s
    );
-- Query: get_video (guest)
SELECT video.*,
    NULL AS last_position_second
FROM video
    JOIN v_channel ON v_channel.channel_id = video.channel_id
WHERE video.video_id = %s
    AND (
        video.privacy = 'public'
        OR video.privacy = 'limited'
    );
-- Query: get_liked_videos
SELECT v.*,
    c.profile_pic_path,
    c.display_name
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
DELETE FROM video
WHERE video_id = %s;