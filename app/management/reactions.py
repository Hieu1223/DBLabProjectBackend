from .db import execute, fetch_one


# -----------------------------
# Video Reactions
# -----------------------------
def set_video_reaction(channel_id: str, video_id: str, reaction: str):
    """
    reaction: 'like', 'dislike', or 'none'
    """
    if reaction not in ("like", "dislike", "none"):
        raise ValueError("reaction must be 'like', 'dislike', or 'none'")

    prev = fetch_one(
        "SELECT reaction_type FROM video_reactions WHERE channel_id = %s AND video_id = %s;",
        (channel_id, video_id),
    )
    prev_reaction = prev["reaction_type"] if prev else "none"

    # Decrement count for previous reaction if it was like/dislike
    if prev_reaction == "like":
        execute(
            "UPDATE video SET like_count = GREATEST(COALESCE(like_count,0) - 1, 0) WHERE video_id = %s;",
            (video_id,),
        )
    elif prev_reaction == "dislike":
        execute(
            "UPDATE video SET dislike_count = GREATEST(COALESCE(dislike_count,0) - 1, 0) WHERE video_id = %s;",
            (video_id,),
        )

    # Update or insert new reaction
    if prev:
        execute(
            "UPDATE video_reactions SET reaction_type = %s WHERE channel_id = %s AND video_id = %s;",
            (reaction, channel_id, video_id),
        )
    else:
        execute(
            "INSERT INTO video_reactions (channel_id, video_id, reaction_type) VALUES (%s, %s, %s);",
            (channel_id, video_id, reaction),
        )

    # Increment count for new reaction if it is like/dislike
    if reaction == "like":
        execute(
            "UPDATE video SET like_count = COALESCE(like_count,0) + 1 WHERE video_id = %s;",
            (video_id,),
        )
    elif reaction == "dislike":
        execute(
            "UPDATE video SET dislike_count = COALESCE(dislike_count,0) + 1 WHERE video_id = %s;",
            (video_id,),
        )


def get_video_reaction(channel_id: str, video_id: str) -> str:
    row = fetch_one(
        "SELECT reaction_type FROM video_reactions WHERE channel_id = %s AND video_id = %s;",
        (channel_id, video_id),
    )
    return row["reaction_type"] if row else "none"


# Comment Reactions
def set_comment_reaction(channel_id: str, comment_id: str, reaction: str):
    """
    reaction: 'like', 'dislike', or 'none'
    """
    if reaction not in ("like", "dislike", "none"):
        raise ValueError("reaction must be 'like', 'dislike', or 'none'")

    prev = fetch_one(
        "SELECT reaction_type FROM comment_reactions WHERE channel_id = %s AND comment_id = %s;",
        (channel_id, comment_id),
    )
    prev_reaction = prev["reaction_type"] if prev else "none"

    # Decrement count for previous reaction
    if prev_reaction == "like":
        execute(
            "UPDATE comment SET like_count = GREATEST(COALESCE(like_count,0) - 1, 0) WHERE comment_id = %s;",
            (comment_id,),
        )
    elif prev_reaction == "dislike":
        execute(
            "UPDATE comment SET dislike_count = GREATEST(COALESCE(dislike_count,0) - 1, 0) WHERE comment_id = %s;",
            (comment_id,),
        )

    # Update or insert reaction
    if prev:
        execute(
            "UPDATE comment_reactions SET reaction_type = %s WHERE channel_id = %s AND comment_id = %s;",
            (reaction, channel_id, comment_id),
        )
    else:
        execute(
            "INSERT INTO comment_reactions (channel_id, comment_id, reaction_type) VALUES (%s, %s, %s);",
            (channel_id, comment_id, reaction),
        )

    # Increment count for new reaction
    if reaction == "like":
        execute(
            "UPDATE comment SET like_count = COALESCE(like_count,0) + 1 WHERE comment_id = %s;",
            (comment_id,),
        )
    elif reaction == "dislike":
        execute(
            "UPDATE comment SET dislike_count = COALESCE(dislike_count,0) + 1 WHERE comment_id = %s;",
            (comment_id,),
        )


def get_comment_reaction(channel_id: str, comment_id: str) -> str:
    row = fetch_one(
        "SELECT reaction_type FROM comment_reactions WHERE channel_id = %s AND comment_id = %s;",
        (channel_id, comment_id),
    )
    return row["reaction_type"] if row else "none"
