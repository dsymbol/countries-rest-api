"""
This test file contains getting country data tests
"""

import pytest

countries = [('Spain', 200),
             ('United States', 200),
             ('Uganda', 404)]


@pytest.mark.parametrize('country, status', countries)
def test_get_country_by_name(country, status, client):
    response = client.get_country_by_name(country)
    assert response.status_code == status


def test_get_country_by_capital(client):
    response = client.get_country_by_capital("Madrid")
    assert 'Spanish' in response.text
    assert response.status_code == 200


def test_get_country_by_invalid_capital(client):
    response = client.get_country_by_capital("Mad")
    assert "Could not find a country with that capital" in response.text
    assert response.status_code == 404


def test_get_country_by_language(client):
    response = client.get_country_by_language("English")
    assert 'United Kingdom' in response.text and 'United States' in response.text
    assert response.status_code == 200


def test_get_country_by_currency(client):
    response = client.get_country_by_currency("EUR")
    assert 'Italian' in response.text
    assert response.status_code == 200


def test_get_all_countries(client):
    countries_list = ["United Kingdom", "English", "SEK", "Hebrew"]
    response = client.get_all_countries()
    result = all(i in response.text for i in countries_list)
    assert result
    assert len(response.json()) == 7
