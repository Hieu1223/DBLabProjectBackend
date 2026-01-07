INSERT INTO comment (
        parent_comment_id,
        video_id,
        channel_id,
        content
    )
VALUES (
        '789e0123-e89b-45d3-b456-426614174111',
        -- parent_comment_id UUID
        '550e8400-e29b-41d4-a716-446655440000',
        -- video_id UUID
        '123e4567-e89b-12d3-a456-426614174000',
        -- channel_id UUID
        'I agree with you! This helped me a lot.'
    )
RETURNING *;