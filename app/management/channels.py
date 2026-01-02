from .db import *

def get_all_channels(page: int = 0, page_size: int = 10):
    
    return fetch_all(
        "SELECT channel_id,display_name FROM channel ORDER BY subscriber_count DESC LIMIT %s OFFSET %s;",
        (page_size, page * page_size)
    )




def get_channel_by_id(channel_id):
    """
    Fetch a channel by ID (no paging needed, unique result)
    """
    return fetch_all(
        "SELECT * FROM channel WHERE channel_id = %s;",
        (channel_id,)
    )


def search_channels(keyword, page: int = 0, page_size: int = 10):
    return fetch_all(
        """
        SELECT channel_id,display_name,profile_pic_path FROM channel
        WHERE LOWER(display_name) LIKE %s
        ORDER BY subscriber_count
        LIMIT %s OFFSET %s;
        """,
        (f"%{keyword.lower()}%", page_size, page * page_size)
    )


def create_channel(display_name, description, profile_pic, auth_token):
    query = """
        INSERT INTO channel (display_name, description, profile_pic_path, auth_token)
        VALUES (%s, %s, %s, %s)
        RETURNING channel_id;
    """
    result = execute(query, (display_name, description, profile_pic, auth_token), fetch_one=True)
    return result["channel_id"] if result else None


def update_channel(
    channel_id,
    description=None,
    display_name=None,
    profile_pic_path=None,
    auth_token=None
):
    fields = []
    values = []

    if description is not None:
        fields.append("description = %s")
        values.append(description)

    if display_name is not None:
        fields.append("display_name = %s")
        values.append(display_name)

    if profile_pic_path is not None:
        fields.append("profile_pic_path = %s")
        values.append(profile_pic_path)

    if auth_token is not None:
        fields.append("auth_token = %s")
        values.append(auth_token)

    if not fields:
        return

    values.append(channel_id)

    query = f"""
        UPDATE channel
        SET {", ".join(fields)}
        WHERE channel_id = %s;
    """

    execute(query, tuple(values))


def delete_channel(channel_id):
    execute("DELETE FROM channel WHERE channel_id = %s;", (channel_id,))
