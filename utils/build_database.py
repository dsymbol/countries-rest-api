import os
import sqlite3
from pathlib import Path

from scrape_data import scrape_population

root_path = str(Path(os.path.abspath(__file__)).parents[1])
countries = ['United States', 'United Kingdom', 'Spain', 'Israel', 'Italy', 'Sweden', 'Greece']
population = scrape_population(countries)
information = [(countries[0], 'Washington', 'English', 'USD', population[0]),
               (countries[1], 'London', 'English', 'GBP', population[1]),
               (countries[2], 'Madrid', 'Spanish', 'EUR', population[2]),
               (countries[3], 'Jerusalem', 'Hebrew', 'ILS', population[3]),
               (countries[4], 'Rome', 'Italian', 'EUR', population[4]),
               (countries[5], 'Stockholm', 'Swedish', 'SEK', population[5]),
               (countries[6], 'Athens', 'Greek', 'EUR', population[6])]

if os.path.exists(f'{root_path}/countries.db'):
    os.remove(f'{root_path}/countries.db')

conn = sqlite3.connect(f'{root_path}/countries.db')
c = conn.cursor()

c.execute("""CREATE TABLE countries (
            name text PRIMARY KEY,
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
