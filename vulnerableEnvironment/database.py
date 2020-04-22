import sqlite3 as sql

conn = sql.connect("user.db")
cur = conn.cursor()

# =================
#  Query execution
# =================
query = ('''CREATE TABLE USERS2
    (username TEXT NOT NULL,
     email TEXT Primary key,
     password TEXT NOT NULL,
     contact  INT);''')
cur.execute(query)

conn.close()