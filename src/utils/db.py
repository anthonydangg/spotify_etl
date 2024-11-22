from contextlib import contextmanager
from dataclasses import dataclass

import psycopg2

hostname = 'localhost'
database = 'postgres'
username = 'anthonydang'
pwd = ''
port_id = '5432'

@contextmanager
def dbconnect():
    try:
        conn = psycopg2.connect( #can take in a string also
            host = hostname,
            dbname = database,
            user = username,
            password = pwd,
            port = port_id)
        cur = conn.cursor()
        script = '''CREATE TABLE IF NOT EXISTS test(
                                        id  int PRIMARY KEY)'''
        cur.execute(script)
        yield cur
        conn.commit()
    except Exception as error:
        print(error) 

    finally:
        cur.close()
        conn.close()



