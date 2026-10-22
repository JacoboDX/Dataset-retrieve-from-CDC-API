import sqlite3

conn = sqlite3.connect('cdccovid.sqlite')
cur = conn.cursor()

with open('analysis_query.sql') as fhand:
    sql = fhand.read()

cur.execute(sql)
for row in cur:
    print(row)


conn.close()