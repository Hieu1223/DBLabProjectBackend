-- File: playlists.py
-- Query: get_playlist_in_channel
select *
from playlist
where channel_id = %s
limit %s offset %s;
-- Query: create_playlist
INSERT INTO playlist (channel_id, playlist_name)
VALUES (%s, %s)
RETURNING *;
-- Query: add_video_to_playlist
INSERT INTO playlist_video (playlist_id, video_id)
VALUES (%s, %s);
-- Query: delete_playlist
DELETE FROM playlist
WHERE playlist_id = %s;
-- Query: remove_video_from_playlist
DELETE FROM playlist_video
WHERE video_id = %s;
-- Query: get_video_in_playlist
select video.video_id,
    title,
    thumbnail_path
from playlist
    natural join playlist_video
    join video on video.video_id = playlist_video.video_id
WHERE playlist.playlist_id = %s
LIMIT %s OFFSET %s;
-- Query: list_playlist_from_video_and_user
select playlist.playlist_id,
    playlist_name
from playlist
    natural join playlist_video
where playlist_video.video_id = %s
    and playlist.channel_id = %s;