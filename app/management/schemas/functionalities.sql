-- =========================
-- QUERY (SELECT)
-- =========================

--authorize
select * from channel
where channel.channel_id = 'blahblah' and channel.auth_token = "ff";

-- Get all channels
SELECT * FROM channel

-- Get all accessible videos and info
SELECT video.*, watch_progress.last_position_second FROM video
join v_channel on v_channel.channel_id = video.channel_id
left join watch_progress ON watch_progress.video_id = video.video_id and watch_progress.channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e'
where video.privacy = 'public' or video.channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e';



-- Get videos from a specific channel
--guest mode
SELECT * FROM video
join v_channel on v_channel.channel_id = video.channel_id
WHERE video.channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e' and
	(video.privacy = 'public' or video.privacy = 'limited');

--user mode
SELECT video.*, last_position_second FROM video
join v_channel on v_channel.channel_id = video.channel_id
left join watch_progress ON watch_progress.video_id = video.video_id and watch_progress.channel_id = 'db988f5a-2a78-4fdd-af15-92fd7022992e'
WHERE video.channel_id = '95992149-ab84-422e-a5d0-8c95a7f54a32' and
	(video.privacy = 'public' or video.privacy = 'limited' 
		or video.channel_id = '95992149-ab84-422e-a5d0-8c95a7f54a32');



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
join v_channel on v_channel.channel_id = video.channel_id
WHERE LOWER(title) LIKE '%jap%';


-- get playlist with channel info and video count 

select playlist.*,v_channel.*, count(playlist_video.*) as video_count from 
(
	select playlist.*, count(playlist_video.*) as video_count
	join playlist_video on playlist_video.playlist_id = playlist.playlist_id
	group by playlist.playlist_id;
) as v
join v_channel on v_channel.channel_id = v.channel_id



-- =========================
-- CREATE (INSERT)
-- =========================

-- Insert a new channel
INSERT INTO channel (display_name, profile_pic_path, auth_token)
VALUES ('New Channel', '/path/to/pic.jpg', 'auth-token');

-- Insert a new video
INSERT INTO video (channel_id, title, description, video_path)
VALUES ('db988f5a-2a78-4fdd-af15-92fd7022992e', 'New Video', 'Video description', '/path/to/video.mp4');

-- Insert a new comment
INSERT INTO comment (video_id, user_id, content)
VALUES ('7319a114-cea4-4be0-b532-c104fe844cda', 'user-id', 'This is a comment');

--create new playlist
insert into playlist(channel_id,playlist_name)
values ('7319a114-cea4-4be0-b532-c104fe844cda', 'play list name')


--insert video into playlist
insert into playlist_video(playlist_id, video_id)
values ('7319a114-cea4-4be0-b532-c104fe844cda','db988f5a-2a78-4fdd-af15-92fd7022992e')


--create watch progress
insert into watch_progress(channel_id, video_id, last_position_second);
values ('fff','fff','fff')
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



--update channel

update channel
set description = ' ',
	auth_token '',
	display_name = '',
	profile_pic_path = ''
where channel_id = 'ff';

--subscribe to channel
insert into "subscription" (channel_id, subscriber_id)
values ('','');
update channel
set subscriber_count = COALESCE(channel.subscriber_count, 0) + 1
where channel_id = '';

--unsubscribe
delete from "subscription"
where "subscription".channel_id = '' and "subscription".subscriber_id = '';
update channel
set subscriber_count = COALESCE(channel.subscriber_count, 0) -1
where channel_id = '';
--trigger: subscriber count cannot be under 0



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


--delete from playlist

delete from playlist
where playlist_id = '...'

delete from playlist_video
where playlist_video.video_id = 'sdsd'



