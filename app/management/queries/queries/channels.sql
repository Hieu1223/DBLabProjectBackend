-- File: channels.py
-- Query: get_all_channels
SELECT channel_id,
    display_name
FROM channel
ORDER BY subscriber_count DESC
LIMIT %s OFFSET %s;
-- Query: get_channel_by_id
SELECT *
FROM channel
WHERE channel_id = %s;
-- Query: search_channels
SELECT channel_id,
    display_name,
    profile_pic_path,
    subscriber_count -- Business rule: Users can't subscribe to themselves
FROM channel
WHERE LOWER(display_name) LIKE %s
ORDER BY subscriber_count DESC
LIMIT %s OFFSET %s;
-- Query: create_channel
INSERT INTO channel (
        display_name,
        description,
        profile_pic_path,
        auth_token
    )
VALUES (%s, %s, %s, %s)
RETURNING channel_id;
-- Query: update_channel (dynamic)
UPDATE channel
SET { comma - separated fields }
WHERE channel_id = %s
RETURNING *;
-- Query: delete_channel
DELETE FROM channel
WHERE channel_id = %s;