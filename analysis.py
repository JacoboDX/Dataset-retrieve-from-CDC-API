import sqlite3
import matplotlib.pyplot as plt

# Connection
conn = sqlite3.connect('cdccovid.sqlite')
cur = conn.cursor()

# Read
with open('analysis_query.sql') as fhand:
    sql = fhand.read()

# data and axis construction
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

# Plot
plt.figure(figsize=(12, 6))
color = 0
for group,ndeaths in data.items():
    plt.plot(axis, ndeaths, label=group, color=plt.cm.viridis_r(color/10))
    color = color + 1
plt.xticks(range(0,45,3), axis[::3], rotation=90)
plt.legend()
plt.title('COVID-19 deaths by age in the USA')
plt.xlabel('Time')
plt.ylabel('Deaths')
plt.tight_layout()
plt.savefig('covid_deaths_by_age.png')
plt.show()
