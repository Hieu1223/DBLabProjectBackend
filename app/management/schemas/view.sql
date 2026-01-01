CREATE OR REPLACE VIEW v_channel AS
SELECT channel_id,
       display_name,
       subscriber_count,
       profile_pic_path,
       created_at
FROM channel