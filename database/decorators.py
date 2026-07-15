from functools import wraps
from psycopg2.extras import RealDictCursor
from .connection import get_connection

def conn_cursor(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        conn = get_connection()
        try:
            with conn:
                with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                    return func(cursor, *args, **kwargs)
        finally:
            conn.close()
    return wrap