"""
This test file contains country updating tests
"""


def test_update_country_full_payload(client, payload):
    r = client.update_country('Spain', payload)
    assert r.status_code == 200
    response = client.get_country_by_name('Spain')
    assert response.json()[0]['capital'] == 'TestCapital'


def test_update_country_partial_payload(client, payload):
    r = client.update_country('Israel', {'language': payload['language'], 'currency': payload['currency']})
    assert r.status_code == 200
    response = client.get_country_by_name('Israel')
    assert response.json()[0]['language'] == 'TestLang' and response.json()[0][
        'currency'] == 'TestCurrency'


def test_update_country_no_payload(client):
    r = client.update_country('United+States', {})
    assert r.status_code == 422
    assert r.json()['message'] == "Missing JSON payload"
