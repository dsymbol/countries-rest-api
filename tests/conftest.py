from utils.countries_client import CountriesClient
import pytest


@pytest.fixture
def client(scope='session'):
    return CountriesClient()


@pytest.fixture
def payload():
    return {'capital': 'TestCapital', 'language': 'TestLang', 'currency': 'TestCurrency', 'population': 12345}