import sqlite3

conn = sqlite3.connect("test.db")
cursor = conn.cursor()

# 🚨 Mauvaise pratique : Concaténation directe des entrées utilisateur dans une requête SQL
username = input("Enter username: ")
query = "SELECT * FROM users WHERE username = '" + username + "';"
cursor.execute(query)  # ❌ Injection SQL possible !

for row in cursor.fetchall():
    print(row)
