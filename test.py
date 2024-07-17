import sqlite3

conn = sqlite3.connect("users.db")
cur = conn.cursor()

username = "Guilherme"
password = 12345
cur.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
user = cur.fetchone()
conn.close()
