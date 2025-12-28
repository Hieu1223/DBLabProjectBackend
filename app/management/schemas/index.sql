-- =========================
-- CHANNEL
-- =========================
CREATE INDEX idx_channel_created_at
ON channel (created_at);

-- =========================
-- VIDEO
-- =========================
CREATE INDEX idx_video_channel_id
ON video (channel_id);

CREATE INDEX idx_video_upload_time
ON video (upload_time DESC);

CREATE INDEX idx_video_privacy
ON video (privacy);

-- For homepage / channel page sorting
CREATE INDEX idx_video_channel_upload
ON video (channel_id, upload_time DESC);

-- =========================
-- COMMENT
-- =========================
CREATE INDEX idx_comment_video_id
ON comment (video_id);

CREATE INDEX idx_comment_parent
ON comment (parent_comment_id);

CREATE INDEX idx_comment_video_time
ON comment (video_id, comment_time DESC);

-- =========================
-- SUBSCRIPTION
-- =========================
CREATE INDEX idx_subscription_subscriber
ON subscription (subscriber_id);

CREATE INDEX idx_subscription_channel
ON subscription (channel_id);

-- =========================
-- PLAYLIST
-- =========================
CREATE INDEX idx_playlist_channel
ON playlist (channel_id);

-- =========================
-- PLAYLIST_VIDEO
-- =========================
CREATE INDEX idx_playlist_video_playlist
ON playlist_video (playlist_id);

CREATE INDEX idx_playlist_video_video
ON playlist_video (video_id);

-- =========================
-- WATCH_PROGRESS
-- =========================
CREATE INDEX idx_watch_progress_channel
ON watch_progress (channel_id);

CREATE INDEX idx_watch_progress_video
ON watch_progress (video_id);
