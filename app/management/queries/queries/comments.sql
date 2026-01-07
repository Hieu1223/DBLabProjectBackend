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
DELETE FROM comment
WHERE comment_id = %s;