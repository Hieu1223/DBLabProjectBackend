-- =========================
-- EXTENSIONS
-- =========================
CREATE EXTENSION IF NOT EXISTS pgcrypto;

-- =========================
-- ENUM TYPES
-- =========================
CREATE TYPE video_privacy AS ENUM ('public', 'private', 'limited');
CREATE TYPE reaction_type_enum AS ENUM ('like', 'dislike','none');
-- =========================
-- CHANNEL (USER / CREATOR)
-- =========================
CREATE TABLE channel (
    channel_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    display_name TEXT NOT NULL,
    profile_pic_path TEXT,
    subscriber_count BIGINT DEFAULT 0,
    description TEXT NOT NULL,
    auth_token TEXT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================
-- VIDEO
-- =========================
CREATE TABLE video (
    video_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID NOT NULL REFERENCES channel(channel_id) ON DELETE CASCADE,

    title TEXT NOT NULL,
    description TEXT,
    upload_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    video_path TEXT NOT NULL,
    thumbnail_path TEXT NOT NULL,

    views_count BIGINT DEFAULT 0,
    like_count BIGINT DEFAULT 0,
    dislike_count BIGINT DEFAULT 0,

    privacy video_privacy DEFAULT 'public'
);

-- =========================
-- COMMENT (WITH REPLIES)
-- =========================
CREATE TABLE comment (
    comment_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    parent_comment_id UUID REFERENCES comment(comment_id) ON DELETE CASCADE,

    video_id UUID NOT NULL REFERENCES video(video_id) ON DELETE CASCADE,
    channel_id UUID NOT NULL REFERENCES channel(channel_id) ON DELETE CASCADE,

    content TEXT NOT NULL,
    like_count BIGINT DEFAULT 0,
    dislike_count BIGINT DEFAULT 0,
    comment_time TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================
-- COMMENT (WITH REPLIES)
-- =========================

drop table video_reactions;
drop table comment_reactions;


CREATE TABLE video_reactions (
    video_id UUID NOT NULL,
    channel_id UUID NOT NULL,
    reaction_type reaction_type_enum,
    PRIMARY KEY (video_id, channel_id)
);

CREATE TABLE comment_reactions (
    comment_id UUID NOT NULL,
    channel_id UUID NOT NULL,
    reaction_type reaction_type_enum,
    PRIMARY KEY (comment_id, channel_id)
);

-- =========================
-- SUBSCRIPTION
-- =========================
CREATE TABLE subscription (
    subscription_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    subscriber_id UUID NOT NULL REFERENCES channel(channel_id) ON DELETE CASCADE,
    channel_id UUID NOT NULL REFERENCES channel(channel_id) ON DELETE CASCADE,
    subscribe_time TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE (subscriber_id, channel_id)
);

-- =========================
-- PLAYLIST
-- =========================
CREATE TABLE playlist (
    playlist_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID NOT NULL REFERENCES channel(channel_id) ON DELETE CASCADE,
    playlist_name TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- =========================
-- PLAYLIST ↔ VIDEO (M:N)
-- =========================
CREATE TABLE playlist_video (
    playlist_video_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    playlist_id UUID NOT NULL REFERENCES playlist(playlist_id) ON DELETE CASCADE,
    video_id UUID NOT NULL REFERENCES video(video_id) ON DELETE CASCADE,

    UNIQUE (playlist_id, video_id)
);

-- =========================
-- WATCH PROGRESS
-- =========================
CREATE TABLE watch_progress (
    history_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    channel_id UUID NOT NULL REFERENCES channel(channel_id) ON DELETE CASCADE,
    video_id UUID NOT NULL REFERENCES video(video_id) ON DELETE CASCADE,

    last_position_second INTEGER DEFAULT 0,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),

    UNIQUE (channel_id, video_id)
);

