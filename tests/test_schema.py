"""
This test file contains schema validation tests
"""

from cerberus import Validator
import pytest


@pytest.fixture
def cer_validate():
    return Validator(schema, require_all=True)


schema = {'name': {'type': 'string'}, 'capital': {'type': 'string'},
          'language': {'type': 'string'}, 'currency': {'type': 'string'},
          'population': {'type': 'integer'}}


def test_one_country_schema(client, cer_validate, country="United States"):
    response = client.get_country_by_name(country).json()
    assert cer_validate.validate(response[0])


def test_all_countries_schema(client, cer_validate):
    response = client.get_all_countries().json()
    for country in response:
        assert cer_validate.validate(country)
