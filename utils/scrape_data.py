import os
from pathlib import Path

import requests
from lxml import html

country_list = []
with open(os.path.join(str(Path(os.path.abspath(__file__)).parents[1]), 'data', 'country_list.txt')) as f:
    for line in f:
        country_list.append(line.rstrip())


def validate_country_name(name):
    index = [i for i, j in enumerate(country_list) if j.lower() == name.lower()]
    if index:
        return country_list[index[0]]


def scrape_population(name):
    url = "https://www.worldometers.info/world-population/population-by-country/"
    response = requests.get(url, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:38.0) '
                                                        'Gecko/20100101 Firefox/38.0'})
    tree = html.fromstring(response.content)

    # # Update country list
    # countries = tree.xpath('//table[@id="example2"] //a')
    # country_list = [country.text for country in countries]
    #
    # with open(f'{root_path}/data/country_list.txt', 'w') as f:
    #     for country in country_list:
    #         f.write(f'{country}\n')

    if type(name) == list:
        l = []
        for i in name:
            population = tree.xpath(f'//table[@id="example2"] //a[text()="{i}"] /parent::td /following-sibling::td[1]')[
                0].text
            l.append(int(population.replace(",", "")))
        return l

    population = tree.xpath(f'//table[@id="example2"] //a[text()="{name}"] /parent::td /following-sibling::td[1]')[
        0].text
    population = int(population.replace(",", ""))
    return population
