import os
import traceback
from contextlib import contextmanager

import psycopg2

hostname = os.getenv('POSTGRES_HOST', '')
db = os.getenv('POSTGRES_DB', '')
username = os.getenv('POSTGRES_USER', '')
pwd = os.getenv('POSTGRES_PASSWORD', '')
port_id = os.getenv('POSTGRES_PORT', 5432)


@contextmanager
def dbconnect():
    conn = None
    cur = None
    try:
        conn = psycopg2.connect(
            host=hostname, dbname=db, user=username, password=pwd, port=port_id
        )
        print(conn.closed)  # 0 if open
        cur = conn.cursor()
        yield cur
        conn.commit()
    except Exception as error:
        print(f'Error: {error}')
        traceback.print_exc()
    finally:
        if cur is not None:
            cur.close()
        if conn is not None:
            conn.close()
