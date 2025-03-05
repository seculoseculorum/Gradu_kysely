import sqlite3

conn = sqlite3.connect('kysely.db')
c = conn.cursor()
for row in c.execute("SELECT * FROM responses"):
    print(row)
conn.close()