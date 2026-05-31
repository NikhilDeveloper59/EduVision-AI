import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("""
SELECT username
FROM users
""")

for row in cursor.fetchall():
    print(row)

conn.close()