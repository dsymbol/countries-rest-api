import requests


class CountriesClient():
    def __init__(self):
        self.BASE_URI = "http://127.0.0.1:5000/api"

    def get_all_countries(self):
        r = requests.get(f'{self.BASE_URI}/country', headers={'Content-Type': 'application/json'})
        return r

    def get_country_by_name(self, name):
        r = requests.get(f'{self.BASE_URI}/country/{name}', headers={'Content-Type': 'application/json'})
        return r

    def get_country_by_capital(self, capital):
        r = requests.get(f'{self.BASE_URI}/capital/{capital}', headers={'Content-Type': 'application/json'})
        return r

    def get_country_by_language(self, language):
        r = requests.get(f'{self.BASE_URI}/language/{language}', headers={'Content-Type': 'application/json'})
        return r

    def get_country_by_currency(self, currency):
        r = requests.get(f'{self.BASE_URI}/currency/{currency}', headers={'Content-Type': 'application/json'})
        return r

    def create_country(self, name, payload):
        p = requests.post(f"{self.BASE_URI}/country/{name}", json=payload, headers={'Content-Type': 'application/json'})
        return p

    def delete_country(self, name):
        d = requests.delete(f"{self.BASE_URI}/country/{name}", headers={'Content-Type': 'application/json'})
        return d

    def update_country(self, name, payload):
        p = requests.put(f"{self.BASE_URI}/country/{name}", json=payload, headers={'Content-Type': 'application/json'})
        return p