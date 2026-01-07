CREATE INDEX idx_video_channel_upload 
ON video (channel_id, upload_time DESC); 
 
CREATE INDEX idx_video_privacy_upload 
ON video (privacy, upload_time DESC);

CREATE INDEX idx_auth_token 
ON channel(auth_token);