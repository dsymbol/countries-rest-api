"""
This test file contains schema validation tests
"""

import pytest
from cerberus import Validator


@pytest.fixture
def c():
    return Validator(schema, require_all=True)


schema = {'name': {'type': 'string'}, 'capital': {'type': 'string'},
          'language': {'type': 'string'}, 'currency': {'type': 'string'},
          'population': {'type': 'integer'}}


def test_one_country_schema(client, c, country="United States"):
    response = client.get_country_by_name(country).json()
    assert c.validate(response[0])


def test_all_countries_schema(client, c):
    response = client.get_all_countries().json()
    for country in response:
        assert c.validate(country)
