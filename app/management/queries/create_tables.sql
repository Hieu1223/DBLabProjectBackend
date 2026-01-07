CREATE EXTENSION IF NOT EXISTS pgcrypto;
CREATE TYPE reaction_type_enum AS ENUM ('like', 'dislike', 'none');
CREATE TYPE video_privacy AS ENUM ('public', 'private', 'limited');
CREATE TABLE channel (
    channel_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name text NOT NULL CHECK (length(display_name) > 0),
    profile_pic_path text,
    subscriber_count bigint NOT NULL DEFAULT 0 CHECK (subscriber_count >= 0),
    description text NOT NULL,
    auth_token text NOT NULL UNIQUE,
    -- hash(username + password)
    created_at timestamptz NOT NULL DEFAULT now()
);
CREATE TABLE video (
    video_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id uuid NOT NULL,
    title text NOT NULL CHECK (length(title) > 0),
    description text,
    upload_time timestamptz NOT NULL DEFAULT now(),
    video_path text NOT NULL,
    thumbnail_path text NOT NULL,
    views_count bigint NOT NULL DEFAULT 0 CHECK (views_count >= 0),
    like_count bigint NOT NULL DEFAULT 0 CHECK (like_count >= 0),
    dislike_count bigint NOT NULL DEFAULT 0 CHECK (dislike_count >= 0),
    privacy video_privacy NOT NULL DEFAULT 'public',
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id) ON DELETE CASCADE
);
CREATE TABLE comment (
    comment_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_comment_id uuid,
    video_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    content text NOT NULL CHECK (length(content) > 0),
    like_count bigint NOT NULL DEFAULT 0 CHECK (like_count >= 0),
    dislike_count bigint NOT NULL DEFAULT 0 CHECK (dislike_count >= 0),
    comment_time timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (video_id) REFERENCES video(video_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id) ON DELETE CASCADE,
    FOREIGN KEY (parent_comment_id) REFERENCES comment(comment_id) ON DELETE CASCADE
);
CREATE TABLE subscription (
    subscription_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    subscriber_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    subscribe_time timestamptz NOT NULL DEFAULT now(),
    UNIQUE (subscriber_id, channel_id),
    FOREIGN KEY (subscriber_id) REFERENCES channel(channel_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id) ON DELETE CASCADE
);
CREATE TABLE playlist (
    playlist_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id uuid NOT NULL,
    playlist_name text NOT NULL CHECK (length(playlist_name) > 0),
    created_at timestamptz NOT NULL DEFAULT now(),
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id) ON DELETE CASCADE
);
CREATE TABLE playlist_video (
    playlist_video_id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    playlist_id uuid NOT NULL,
    video_id uuid NOT NULL,
    UNIQUE (playlist_id, video_id),
    FOREIGN KEY (playlist_id) REFERENCES playlist(playlist_id) ON DELETE CASCADE,
    FOREIGN KEY (video_id) REFERENCES video(video_id) ON DELETE CASCADE
);
CREATE TABLE video_reactions (
    video_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    reaction_type reaction_type_enum NOT NULL,
    PRIMARY KEY (video_id, channel_id),
    FOREIGN KEY (video_id) REFERENCES video(video_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id) ON DELETE CASCADE
);
CREATE TABLE comment_reactions (
    comment_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    reaction_type reaction_type_enum NOT NULL,
    PRIMARY KEY (comment_id, channel_id),
    FOREIGN KEY (comment_id) REFERENCES comment(comment_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id) ON DELETE CASCADE
);
CREATE TABLE watch_progress (
    video_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    last_position_second integer NOT NULL CHECK (last_position_second >= 0),
    updated_at timestamptz NOT NULL DEFAULT now(),
    PRIMARY KEY (video_id, channel_id),
    FOREIGN KEY (video_id) REFERENCES video(video_id) ON DELETE CASCADE,
    FOREIGN KEY (channel_id) REFERENCES channel(channel_id) ON DELETE CASCADE
);
-- entity user consists both registered users (channel entity) and unregistered
-- unregistered -> no data needs to be stored -> no need for a table