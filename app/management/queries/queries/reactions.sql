-- File: reactions.py
-- Query: get video reaction
SELECT reaction_type
FROM video_reactions
WHERE channel_id = %s
    AND video_id = %s;
-- Query: decrement video like count
UPDATE video
SET like_count = GREATEST(COALESCE(like_count, 0) - 1, 0)
WHERE video_id = %s
RETURNING like_count;
-- Query: decrement video dislike count
UPDATE video
SET dislike_count = GREATEST(COALESCE(dislike_count, 0) - 1, 0)
WHERE video_id = %s
RETURNING dislike_count;
-- Query: update video reaction
UPDATE video_reactions
SET reaction_type = %s
WHERE channel_id = %s
    AND video_id = %s;
-- Query: insert video reaction
INSERT INTO video_reactions (channel_id, video_id, reaction_type)
VALUES (%s, %s, %s);
-- Query: increment video like count
UPDATE video
SET like_count = COALESCE(like_count, 0) + 1
WHERE video_id = %s;
-- Query: increment video dislike count
UPDATE video
SET dislike_count = COALESCE(dislike_count, 0) + 1
WHERE video_id = %s;
-- Query: get comment reaction
SELECT reaction_type
FROM comment_reactions
WHERE channel_id = %s
    AND comment_id = %s;
-- Query: decrement comment like count
UPDATE comment
SET like_count = GREATEST(COALESCE(like_count, 0) - 1, 0)
WHERE comment_id = %s;
-- Query: decrement comment dislike count
UPDATE comment
SET dislike_count = GREATEST(COALESCE(dislike_count, 0) - 1, 0)
WHERE comment_id = %s;
-- Query: update comment reaction
UPDATE comment_reactions
SET reaction_type = %s
WHERE channel_id = %s
    AND comment_id = %s;
-- Query: insert comment reaction
INSERT INTO comment_reactions (channel_id, comment_id, reaction_type)
VALUES (%s, %s, %s);
-- Query: increment comment like count
UPDATE comment
SET like_count = COALESCE(like_count, 0) + 1
WHERE comment_id = %s;
-- Query: increment comment dislike count
UPDATE comment
SET dislike_count = COALESCE(dislike_count, 0) + 1
WHERE comment_id = %s;