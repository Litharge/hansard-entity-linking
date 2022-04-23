import sqlite3
import datetime
from pprint import pprint


conn = sqlite3.connect("test.db",
                       detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

cursor = conn.cursor()

with conn:
    cursor.execute("SELECT * FROM mps")
    print("mps")
    pprint(cursor.fetchall())

    cursor.execute("SELECT * FROM mp_offices")
    print("mp_offices")
    pprint(cursor.fetchall())