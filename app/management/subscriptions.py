from .db import *

def subscribe_channel(channel_id: str, subscriber_id: str):
    try:
        execute(
            """
            INSERT INTO "subscription" (channel_id, subscriber_id)
            VALUES (%s, %s);
            """,
            (channel_id, subscriber_id)
        )

        execute(
            """
            UPDATE channel
            SET subscriber_count = COALESCE(subscriber_count, 0) + 1
            WHERE channel_id = %s;
            """,
            (channel_id,)
        )

    except Exception as e:
        raise e


def unsubscribe_channel(channel_id: str, subscriber_id: str):
    try:
        execute(
            """
            DELETE FROM "subscription"
            WHERE channel_id = %s AND subscriber_id = %s;
            """,
            (channel_id, subscriber_id)
        )

        execute(
            """
            UPDATE channel
            SET subscriber_count = COALESCE(subscriber_count, 0) - 1
            WHERE channel_id = %s;
            """,
            (channel_id,)
        )

    except Exception as e:
        raise e
