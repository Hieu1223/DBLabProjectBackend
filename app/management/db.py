import psycopg2
from psycopg2.extras import RealDictCursor

DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "dbname": "videos",
    "user": "postgres",
    "password": "Keqingsimp@01.",
}


def get_connection():
    return psycopg2.connect(**DB_CONFIG)


def fetch_all(query, params=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchall()


def fetch_one(query, params=None):
    with get_connection() as conn:
        with conn.cursor(cursor_factory=RealDictCursor) as cur:
            cur.execute(query, params)
            return cur.fetchone()


def execute(query, params=None, fetch_one=False):
    with get_connection() as conn:
        cursor_factory = RealDictCursor if fetch_one else None
        with conn.cursor(cursor_factory=cursor_factory) as cur:
            cur.execute(query, params)
            conn.commit()
            if fetch_one:
                return cur.fetchone()
