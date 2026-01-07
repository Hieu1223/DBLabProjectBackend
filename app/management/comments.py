from .db import fetch_all, execute


def get_comments(video_id, page=0, page_size=10):
    query = """
    SELECT *
    FROM comment
    WHERE video_id = %s
    ORDER BY comment_time DESC
    LIMIT %s OFFSET %s;
    """
    return fetch_all(query, (video_id, page_size, page * page_size))


def create_comment(video_id, user_id, content):
    return execute(
        """
        INSERT INTO comment (video_id, channel_id, content)
        VALUES (%s, %s, %s)
        RETURNING *;
        """,
        (video_id, user_id, content),
        fetch_one=True,
    )


def update_comment(comment_id, content):
    return execute(
        """
        UPDATE comment
        SET content = %s,
            comment_time = NOW()
        WHERE comment_id = %s
        RETURNING *;
        """,
        (content, comment_id),
        fetch_one=True,
    )


def like_comment(comment_id):
    execute(
        """
        UPDATE comment
        SET like_count = COALESCE(like_count, 0) + 1
        WHERE comment_id = %s;
        """,
        (comment_id,),
    )


def dislike_comment(comment_id):
    execute(
        """
        UPDATE comment
        SET dislike_count = COALESCE(dislike_count, 0) + 1
        WHERE comment_id = %s;
        """,
        (comment_id,),
    )


def delete_comment(comment_id):
    execute("DELETE FROM comment WHERE comment_id = %s;", (comment_id,))
