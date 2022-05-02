"""
This test file contains country creation tests
"""


def test_creating_country(client, payload):
    r = client.create_country('Egypt', payload)
    assert r.status_code == 201
    response = client.get_country_by_name('Egypt')
    assert response.json()[0]['language'] == 'TestLang'
    assert "Country created" in r.text


def test_creating_invalid_country(client, payload):
    r = client.create_country('Test_Country_1', payload)
    assert "country_list.txt" in r.json()['message']


def test_creating_country_no_payload(client):
    r = client.create_country('Uganda', {})
    assert r.status_code == 422
    assert "required field" in r.text


def test_creating_country_invalid_payload(client):
    r = client.create_country('Jordan', {"Hello": "World"})
    assert r.status_code == 422
    assert "unknown field" in r.text
