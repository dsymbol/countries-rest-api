from pathlib import Path
import sqlite3
import os

root_path = str(Path(__file__).parents[1])
information = [('United States', 'Washington', 'English', 'USD', 334_454_094),
               ('United Kingdom', 'London', 'English', 'GBP', 68_519_283),
               ('Spain', 'Madrid', 'Spanish', 'EUR', 46_786_601),
               ('Israel', 'Jerusalem', 'Hebrew', 'ILS', 8_901_435),
               ('Italy', 'Rome', 'Italian', 'EUR', 60_306_224),
               ('Sweden', 'Stockholm', 'Swedish', 'SEK', 10_211_335),
               ('Greece', 'Athens', 'Greek', 'EUR', 10_334_599)]

if os.path.exists(f'{root_path}/countries.db'):
    os.remove(f'{root_path}/countries.db')

conn = sqlite3.connect(f'{root_path}/countries.db')
c = conn.cursor()

c.execute("""CREATE TABLE countries (
            name text,
            capital text,
            language text,
            currency text,
            population integer
            )""")

for info in information:
    with conn:
        c.execute("INSERT INTO countries VALUES (:name, :capital, :language, :currency, :population)",
                  {'name': info[0], 'capital': info[1], 'language': info[2], 'currency': info[3],
                   'population': info[4]})
