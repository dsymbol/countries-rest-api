import os
import sqlite3
from pathlib import Path

from cerberus import Validator

DATABASE_PATH = os.path.join(str(Path(os.path.abspath(__file__)).parents[1]), 'countries.db')

if not os.path.exists(DATABASE_PATH):
    raise Exception("Database file not found")

conn = sqlite3.connect(DATABASE_PATH, check_same_thread=False)
c = conn.cursor()


def format_data(tpl):
    """
    Returns formatted data in easily accessible dictionary format
    """
    name, capital, language, currency, population = tpl
    return {'name': name, 'capital': capital, 'language': language, 'currency': currency, 'population': population}


def get_all_countries(gt: int = None, lt: int = None):
    """
    Returns all countries and their data
    """
    if gt and not lt:
        c.execute("SELECT * FROM countries WHERE population > :gt", {'gt': gt})
        result = c.fetchall()
    elif lt and not gt:
        c.execute("SELECT * FROM countries WHERE population < :lt", {'lt': lt})
        result = c.fetchall()
    elif gt and lt:
        c.execute("SELECT * FROM countries WHERE population > :gt AND population < :lt", {'gt': gt, 'lt': lt})
        result = c.fetchall()
    else:
        c.execute("SELECT * FROM countries")
        result = c.fetchall()
    data = []
    [data.append(format_data(i)) for i in result if result]
    return data


def get_country(name=None, language=None, currency=None, capital=None):
    """
    Returns a country based on passed in arg
    """
    if name:
        c.execute("SELECT * FROM countries WHERE LOWER(name)=:name", {'name': name.lower()})
    elif language:
        c.execute("SELECT * FROM countries WHERE LOWER(language)=:language", {'language': language.lower()})
    elif currency:
        c.execute("SELECT * FROM countries WHERE LOWER(currency)=:currency", {'currency': currency.lower()})
    elif capital:
        c.execute("SELECT * FROM countries WHERE LOWER(capital)=:capital", {'capital': capital.lower()})
    result = c.fetchall()

    data = []
    [data.append(format_data(i)) for i in result if result]
    return data


def create_country(name,
                   d: dict):
    """
    Creates a country by name based on passed in data
    """
    schema = {'capital': {'type': 'string'}, 'language': {'type': 'string'}, 'currency': {'type': 'string'},
              'population': {'type': 'integer'}}
    v = Validator(schema, require_all=True)
    result = v.validate(d)
    errors = v.errors
    if not result:
        return result, errors

    with conn:
        c.execute("INSERT INTO countries VALUES (:name, :capital, :language, :currency, :population)",
                  {'name': name, 'capital': d['capital'], 'language': d['language'], 'currency': d['currency'],
                   'population': d['population']})
    return result, errors


def delete_country(name):
    """
    Deletes a country by name
    """
    with conn:
        c.execute("DELETE from countries WHERE LOWER(name) = :name", {'name': name.lower()})


def update_country(name, d: dict):
    """
    Updates a country by name based on passed in data
    """
    schema = {'capital': {'type': 'string'}, 'language': {'type': 'string'}, 'currency': {'type': 'string'},
              'population': {'type': 'integer'}}
    v = Validator(schema, require_all=True)
    result = v.validate(d)
    errors = v.errors

    if not result:
        return result, errors

    c.execute("""UPDATE countries SET name = :name, capital = :capital, language = :language, currency = :currency, 
                population = :population WHERE LOWER(name) = :name""",
              {'name': name.lower(), 'capital': d['capital'], 'language': d['language'], 'currency': d['currency'],
               'population': d['population']})
    return result, errors


def partially_update_country(name, d: dict):
    """
    Updates a country by name based on passed in data
    """
    schema = {'capital': {'type': 'string'}, 'language': {'type': 'string'}, 'currency': {'type': 'string'},
              'population': {'type': 'integer'}}
    v = Validator(schema)
    result = v.validate(d)
    errors = v.errors

    if not result:
        return result, errors

    if 'capital' in d.keys():
        with conn:
            c.execute("""UPDATE countries SET capital = :capital WHERE LOWER(name) = :name""",
                      {'name': name.lower(), 'capital': d['capital']})
    if 'language' in d.keys():
        with conn:
            c.execute("""UPDATE countries SET language = :language WHERE LOWER(name) = :name""",
                      {'name': name.lower(), 'language': d['language']})
    if 'currency' in d.keys():
        with conn:
            c.execute("""UPDATE countries SET currency = :currency WHERE LOWER(name) = :name""",
                      {'name': name.lower(), 'currency': d['currency']})
    if 'population' in d.keys():
        with conn:
            c.execute("""UPDATE countries SET population = :population WHERE LOWER(name) = :name""",
                      {'name': name.lower(), 'population': d['population']})
    return result, errors
