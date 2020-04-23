
import sqlite3
with sqlite3.connect('test.db') as connection:

	c = connection.cursor()
	c.execute('''CREATE TABLE USERS2
    (username TEXT NOT NULL,
     email TEXT Primary key,
     password TEXT NOT NULL,
     contact  INT);''')






