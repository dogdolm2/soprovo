import sqlite3

connection1 = sqlite3.connect('users.db')
connection2 = sqlite3.connect('trips.db')

cursor1 = connection1.cursor()
cursor2 = connection2.cursor()


cursor1.execute('''
CREATE TABLE IF NOT EXISTS Users (
id INTEGER PRIMARY KEY,
verifytag TEXT NOT NULL,
email TEXT NOT NULL,
password TEXT NOT NULL,
whitelisted INTEGER,
namea TEXT NOT NULL,
nameb TEXT NOT NULL,
namec TEXT NOT NULL
)
''')

# 0 - id
# 1 - destination
# 2 - description
# 3 - class
# 4 - price
# 5 - state
# 6 - quantity
# 7 - participants

cursor2.execute('''
CREATE TABLE IF NOT EXISTS Trips (
id INTEGER PRIMARY KEY,
destination TEXT NOT NULL,
description TEXT NOT NULL,
class TEXT NOT NULL,
price TEXT NOT NULL,
state TEXT NOT NULL,
quantity TEXT NOT NULL,
participants TEXT
)
''')

connection1.commit()
connection2.commit()

connection1.close()
connection2.close()
