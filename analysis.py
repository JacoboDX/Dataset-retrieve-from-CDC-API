import sqlite3

conn = sqlite3.connect('cdccovid.sqlite')
cur = conn.cursor()

with open('analysis_query.sql') as fhand:
    sql = fhand.read()

cur.execute(sql)
data = dict()
axis = list()
for row in cur:
    # print(row)
    age_group = row[2]
    deaths = row[3]
    if age_group not in data:
        data[age_group] = list()
    data[age_group].append(deaths)
    syear = str(row[0])
    smonth = str(row[1]).zfill(2)
    date = syear + '-' + smonth
    if date not in axis:
        axis.append(date)


# print(data)
# print(axis)
# print(len(data))
# print(len(axis))

conn.close()