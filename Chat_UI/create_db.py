import sqlite3

con = sqlite3.connect("database.db")
cur = con.cursor()

cur.execute("""
CREATE TABLE users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    email TEXT,
    password TEXT
)
""")

con.commit()
con.close()

print("Database Created Successfully")
