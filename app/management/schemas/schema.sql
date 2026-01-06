-- 1. Enable UUID support and Types
CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TYPE reaction_type_enum AS ENUM ('like', 'dislike', 'none');
CREATE TYPE video_privacy AS ENUM ('public', 'private', 'limited');

-- 2. Create Tables without constraints
CREATE TABLE channel (
    channel_id uuid DEFAULT gen_random_uuid(),
    display_name text NOT NULL,
    profile_pic_path text,
    subscriber_count bigint DEFAULT 0,
    description text NOT NULL,
    auth_token text,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE video (
    video_id uuid DEFAULT gen_random_uuid(),
    channel_id uuid NOT NULL,
    title text NOT NULL,
    description text,
    upload_time timestamp with time zone DEFAULT now(),
    video_path text NOT NULL,
    thumbnail_path text NOT NULL,
    views_count bigint DEFAULT 0,
    like_count bigint DEFAULT 0,
    dislike_count bigint DEFAULT 0,
    privacy video_privacy DEFAULT 'public'
);

CREATE TABLE comment (
    comment_id uuid DEFAULT gen_random_uuid(),
    parent_comment_id uuid,
    video_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    content text NOT NULL,
    like_count bigint DEFAULT 0,
    dislike_count bigint DEFAULT 0,
    comment_time timestamp with time zone DEFAULT now()
);

CREATE TABLE subscription (
    subscription_id uuid DEFAULT gen_random_uuid(),
    subscriber_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    subscribe_time timestamp with time zone DEFAULT now()
);

CREATE TABLE playlist (
    playlist_id uuid DEFAULT gen_random_uuid(),
    channel_id uuid NOT NULL,
    playlist_name text NOT NULL,
    created_at timestamp with time zone DEFAULT now()
);

CREATE TABLE video_reactions (
    video_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    reaction_type reaction_type_enum
);


CREATE TABLE playlist_video (
    playlist_video_id uuid DEFAULT gen_random_uuid() NOT NULL,
    playlist_id uuid NOT NULL,
    video_id uuid NOT NULL
);


CREATE TABLE comment_reactions (
    comment_id uuid NOT NULL,
    channel_id uuid NOT NULL,
    reaction_type reaction_type_enum
);