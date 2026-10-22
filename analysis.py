import sqlite3

conn = sqlite3.connect('cdccovid.sqlite')
cur = conn.cursor()

with open('analysis_query.sql') as fhand:
    sql = fhand.read()

cur.execute(sql)
data = dict()
for row in cur:
    # print(row)
    age_group = row[2]
    deaths = row[3]
    if age_group not in data:
        data[age_group] = list()
    data[age_group].append(deaths)


print(data)

conn.close()