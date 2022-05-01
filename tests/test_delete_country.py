"""
This test file contains country deletion tests
"""

import pytest


to_delete = [('United Kingdom', 200),
             ('United States', 200),
             ('Israel', 200)]


@pytest.mark.parametrize('country, status', to_delete)
def test_delete_country(country, status, client):
    r = client.delete_country(country)
    assert r.status_code == status


def test_delete_invalid_country(client):
    r = client.delete_country('Uganda')
    assert r.status_code == 404
    assert r.json()["message"] == "Not Found"
