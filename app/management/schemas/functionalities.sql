-- =========================
-- QUERY (SELECT)
-- =========================

-- Get all channels
SELECT * FROM channel;

-- Get all accessible videos
SELECT * FROM video
where video.privacy = 'public' or video.channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e'
;

-- Get videos from a specific channel
SELECT * FROM video
WHERE video.channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e' and
	(video.privacy = 'public' or video.privacy = 'limited');


SELECT * FROM video
WHERE video.channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e' and
	(video.privacy = 'public' or video.privacy = 'limited' or video.channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e');



-- Get comments from a specific video
SELECT * FROM comment 
WHERE comment.video_id = '7319a114-cea4-4be0-b532-c104fe844cda';

-- Get a specific channel
SELECT * FROM channel
WHERE channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e';

-- Search channels by display name (case-insensitive)
SELECT * FROM channel
WHERE LOWER(channel.display_name) LIKE '%bl%';

-- Search videos by title (case-insensitive)
SELECT * FROM video
WHERE LOWER(title) LIKE '%jap%';


-- =========================
-- CREATE (INSERT)
-- =========================

-- Insert a new channel
INSERT INTO channel (channel_id, subscriber_count, display_name, profile_pic_path, created_at, auth_token)
VALUES ('new-channel-id', 0, 'New Channel', '/path/to/pic.jpg', NOW(), 'auth-token');

-- Insert a new video
INSERT INTO video (video_id, channel_id, title, description, upload_time, video_path)
VALUES ('new-video-id', 'db988f5a-2a78-4fdd-af15-92fd7022992e', 'New Video', 'Video description', NOW(), '/path/to/video.mp4');

-- Insert a new comment
INSERT INTO comment (comment_id, video_id, user_id, content, created_at)
VALUES ('new-comment-id', '7319a114-cea4-4be0-b532-c104fe844cda', 'user-id', 'This is a comment', NOW());





-- =========================
-- UPDATE VIDEO LIKES/DISLIKES
-- =========================

-- Like a video (increment likes)
UPDATE video
SET likes_count = COALESCE(likes_count, 0) + 1
WHERE video_id = '7319a114-cea4-4be0-b532-c104fe844cda';

-- Dislike a video (increment dislikes)
UPDATE video
SET dislikes_count = COALESCE(dislikes_count, 0) + 1
WHERE video_id = '7319a114-cea4-4be0-b532-c104fe844cda';


-- =========================
-- UPDATE COMMENT LIKES/DISLIKES AND TIMESTAMP
-- =========================

-- Update comment content and update timestamp
UPDATE comment
SET content = 'Updated comment content',
    updated_at = NOW()
WHERE comment_id = 'comment-id-to-update';

-- Like a comment
UPDATE comment
SET likes_count = COALESCE(likes_count, 0) + 1
WHERE comment_id = 'comment-id-to-update';

-- Dislike a comment
UPDATE comment
SET dislikes_count = COALESCE(dislikes_count, 0) + 1
WHERE comment_id = 'comment-id-to-update';








-- =========================
-- DELETE
-- =========================

-- Delete a specific channel
DELETE FROM channel
WHERE channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e';

-- Delete a specific video
DELETE FROM video
WHERE video_id = '7319a114-cea4-4be0-b532-c104fe844cda';

-- Delete a specific comment
DELETE FROM comment
WHERE comment_id = 'comment-id-to-delete';
