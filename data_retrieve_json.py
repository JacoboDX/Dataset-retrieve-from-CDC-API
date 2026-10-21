import urllib.request, urllib.parse, urllib.error
import json
import sqlite3
import ssl

ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

conn = sqlite3.connect('cdccovid.sqlite')
cur = conn.cursor()

def textoanumero(valor):
    if valor is not None:
        return int(valor)
    else:
        return None

cur.executescript('''

CREATE TABLE IF NOT EXISTS metodo (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    metodo TEXT UNIQUE 
);
    
CREATE TABLE IF NOT EXISTS state (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    state TEXT UNIQUE 
);

CREATE TABLE IF NOT EXISTS sex (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    sex TEXT UNIQUE 
);

CREATE TABLE IF NOT EXISTS age_group (
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
    age_group TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS Dataset (
    data_as_of TEXT,
    start_date TEXT,
    end_date TEXT,
    metodo_id INTEGER,
    state_id INTEGER,
    sex_id INTEGER, 
    age_group_id INTEGER, 
    covid_19_deaths INTEGER, 
    total_deaths INTEGER, 
    pneumonia_deaths INTEGER, 
    pneumonia_and_covid_19_deaths INTEGER, 
    influenza_deaths INTEGER, 
    pneumonia_influenza_or_covid INTEGER,
    year INTEGER,
    month INTEGER,
    footnote TEXT
)
''')

url = input('Enter URL: ')
if len(url) < 1 :
    url = 'https://data.cdc.gov/resource/9bhg-hcku.json'

cur.execute('SELECT COUNT(*) FROM Dataset')
row = cur.fetchone()

offset = row[0]
limit = 1000

cont = 0
desc = input('How many pages of 1,000 rows do you want to download? (Enter = all) ')
if len(desc) < 1: desc = '0'
idesc = int(desc)

while True:
    parametros = {'$limit': limit, '$offset': offset, '$order': ':id'}
    urlfinal = url + '?' + urllib.parse.urlencode(parametros)
    print(urlfinal)
    urlhand = urllib.request.urlopen(urlfinal, context=ctx)
    data = urlhand.read().decode()
    json_data = json.loads(data)
    if len(json_data) < 1 : break
    for fila in json_data:
        try:
            data_as_of = fila['data_as_of']
            start_date = fila['start_date']
            end_date = fila['end_date']
            metodo = fila['group']
            state = fila['state']
            sex = fila['sex']
            age_group = fila['age_group']
            covid_19_deaths = textoanumero(fila.get('covid_19_deaths'))
            total_deaths = textoanumero(fila.get('total_deaths'))
            pneumonia_deaths = textoanumero(fila.get('pneumonia_deaths'))
            pneumonia_and_covid_19_deaths = textoanumero(fila.get('pneumonia_and_covid_19_deaths'))
            influenza_deaths = textoanumero(fila.get('influenza_deaths'))
            pneumonia_influenza_or_covid = textoanumero(fila.get('pneumonia_influenza_or_covid'))
            year = textoanumero(fila.get('year'))
            month = textoanumero(fila.get('month'))
            footnote = fila.get('footnote')
        except:
            print('Unexpected format')
            continue
  
        cur.execute('''INSERT OR IGNORE INTO metodo (metodo)
            VALUES ( ? )''', ( metodo, ) )
        cur.execute('SELECT id FROM metodo WHERE metodo = ? ', (metodo, ))
        metodo_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO state (state)
            VALUES ( ? )''', ( state, ) )
        cur.execute('SELECT id FROM state WHERE state = ? ', (state, ))
        state_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO sex (sex)
            VALUES ( ? )''', ( sex, ) )
        cur.execute('SELECT id FROM sex WHERE sex = ? ', (sex, ))
        sex_id = cur.fetchone()[0]

        cur.execute('''INSERT OR IGNORE INTO age_group (age_group)
            VALUES ( ? )''', ( age_group, ) )
        cur.execute('SELECT id FROM age_group WHERE age_group = ? ', (age_group, ))
        age_group_id = cur.fetchone()[0]
    
        cur.execute('''INSERT OR IGNORE INTO Dataset (data_as_of, start_date, end_date, metodo_id, state_id, sex_id, age_group_id, covid_19_deaths, total_deaths, pneumonia_deaths, pneumonia_and_covid_19_deaths, influenza_deaths, pneumonia_influenza_or_covid, year, month, footnote)
                VALUES ( ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )''', ( data_as_of, start_date, end_date, metodo_id, state_id, sex_id, age_group_id, covid_19_deaths, total_deaths, pneumonia_deaths, pneumonia_and_covid_19_deaths, influenza_deaths, pneumonia_influenza_or_covid, year, month, footnote) )

    conn.commit()
    print(offset)
    offset = offset + limit
    cont = cont + 1
    if cont == idesc: break 

print(urlfinal)
conn.commit()