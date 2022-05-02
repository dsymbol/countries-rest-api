import pytest

from utils.countries_client import CountriesClient


@pytest.fixture
def client():
    return CountriesClient()


@pytest.fixture
def payload():
    return {'capital': 'TestCapital', 'language': 'TestLang', 'currency': 'TestCurrency'}
