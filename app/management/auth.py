from .db import *
import hashlib


def authorize_channel(channel_id: str, token: str) -> bool:
    result = fetch_all(
        "SELECT 1 FROM channel WHERE channel_id = %s AND auth_token = %s LIMIT 1;",
        (channel_id, token)
    )
    return bool(result)


def authorize_video(video_id: str, token: str) -> bool:
    result = fetch_all(
        """
        SELECT 1
        FROM channel
        JOIN video ON video.channel_id = channel.channel_id
        WHERE channel.auth_token = %s AND video.video_id = %s
        LIMIT 1;
        """,
        (token, video_id)
    )
    return bool(result)


def authorize_playlist(playlist_id: str, auth_token: str) -> bool:
    query = """
    SELECT 1
    FROM playlist p
    JOIN channel c ON c.channel_id = p.channel_id
    WHERE c.auth_token = %s
      AND p.playlist_id = %s
    LIMIT 1;
    """
    return fetch_one(query, (auth_token, playlist_id)) is not None


def authorize_comment(comment_id: str, token: str) -> bool:
    result = fetch_all(
        """
        SELECT 1
        FROM channel
        JOIN comment ON comment.channel_id = channel.channel_id
        WHERE channel.auth_token = %s AND comment.comment_id = %s
        LIMIT 1;
        """,
        (token, comment_id)
    )
    return bool(result)


def authorize_subscription(subscription_id: str, token: str) -> bool:
    result = fetch_all(
        """
        SELECT 1
        FROM channel
        JOIN subscription ON subscription.subscriber_id = channel.channel_id
        WHERE channel.auth_token = %s AND subscription.subscriber_id = %s
        LIMIT 1;
        """,
        (token, subscription_id)
    )
    return bool(result)


def create_auth_token(username: str, password: str) -> str:
    raw = f"{username}{password}"
    token = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    return token



def get_id_from_token(token: str):
    query = """
        SELECT channel_id
        FROM channel
        WHERE auth_token = %s;
    """
    result = fetch_one(query, (token,))
    return result["channel_id"] if result else None
