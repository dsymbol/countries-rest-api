"""
lt = lower than; gt = greater than
"""


def test_get_lt_population(client):
    lt = 9000000
    response = client.get_country_by_population(lt=lt)
    assert response.status_code == 200
    for i in response.json():
        assert i["population"] < lt


def test_get_gt_population(client):
    gt = 47754778
    response = client.get_country_by_population(gt=gt)
    assert response.status_code == 200
    for i in response.json():
        assert i["population"] > gt


def test_get_lt_gt_population(client):
    lt = 321002651
    gt = 47754778
    response = client.get_country_by_population(gt=gt, lt=lt)
    assert response.status_code == 200
    for i in response.json():
        assert lt > i["population"] > gt
        assert i["currency"] == "EUR" or i["currency"] == "GBP"
