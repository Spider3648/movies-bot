import sqlite3
db = sqlite3.connect('Kino.db')
cur = db.cursor()

select_all = "SELECT * FROM Kino"
cur.execute(select_all)
rows = cur.fetchall()

# Вивести результати
for row in rows:
    print(row)
