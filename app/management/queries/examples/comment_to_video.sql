WITH new_comment AS (
    INSERT INTO comment (
            video_id,
            channel_id,
            content
        )
    VALUES (
            '550e8400-e29b-41d4-a716-446655440000',
            -- video_id UUID
            '123e4567-e89b-12d3-a456-426614174000',
            -- channel_id UUID
            'This is an amazing video tutorial!'
        )
    RETURNING comment_id,
        comment_time
)
SELECT c.comment_id,
    c.content,
    c.comment_time,
    ch.display_name as author_name,
    ch.profile_pic_path
FROM new_comment nc
    JOIN comment c ON nc.comment_id = c.comment_id
    JOIN channel ch ON c.channel_id = ch.channel_id;