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
WHERE channel_id = %s
    AND subscriber_id = %s;
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
WHERE s.subscriber_id = %s
    and s.channel_id = %s;