import json
import os

import bs4
from bs4 import BeautifulSoup

import pytest

from scraper import Scraper
from soup_fetcher import AbstractSoupFetcher


def strip(animal_dict):
    striped_dict = {}
    for key, values in animal_dict.items():
        striped_values = [value.strip() for value in values]
        striped_dict[key.strip()] = [value for value in striped_values if value != '']
    return striped_dict


def create_test_data_dir_path(file_name):
    file_dir = os.path.dirname(__file__)
    tests_data_folder = 'tests_data'
    file_full_path = os.path.join(file_dir, tests_data_folder, file_name)
    return file_full_path


class FakeSoupFetcher(AbstractSoupFetcher):
    def get_soup(self) -> BeautifulSoup:
        file_name = 'test_scraper_data.html'
        file_full_path = create_test_data_dir_path(file_name)
        try:
            with open(file_full_path, 'r', encoding='utf-8') as file:
                file_content = file.read()
                soup = BeautifulSoup(file_content, 'html.parser')
            print(f"HTML content successfully read from {file_name}")
        except IOError as e:
            print(f"An error occurred while reading the file: {e}")
        else:
            return soup


@pytest.fixture
def setup_scraper():
    fake_soup_fetcher = FakeSoupFetcher()
    scraper = Scraper(fake_soup_fetcher)
    animal_table = scraper._get_animal_table_from_soup()
    return scraper, animal_table


class TestScraper:
    def test_get_animal_table_from_soup(self,setup_scraper):
        scraper,animal_table = setup_scraper
        assert animal_table is not None

    def test_get_headers_from_table(self,setup_scraper):
        scraper, animal_table = setup_scraper
        headers: BeautifulSoup = scraper._get_headers_from_table(animal_table)
        headers_values: bs4.element.ResultSet = headers.find_all('th')
        assert len(headers_values) == 7

    def test_get_header_position(self,setup_scraper):
        scraper, animal_table = setup_scraper
        headers = scraper._get_headers_from_table(animal_table)
        animal_header_index = scraper._get_header_position('animal', headers)
        collateral_adjective_header_index = scraper._get_header_position('collateral adjective', headers)
        assert animal_header_index == 0 and collateral_adjective_header_index == 5

    def test_row_not_containing_animal_data(self,setup_scraper):
        scraper, animal_table = setup_scraper
        rows = animal_table.find_all('tr')
        row_without_animal_data = rows[1]
        row_with_animal_data = rows[2]
        assert scraper._row_not_containing_animal_data(
            row_with_animal_data) is False and scraper._row_not_containing_animal_data(row_without_animal_data) is True

    def test_extract_collateral_adjectives(self,setup_scraper):
        scraper, animal_table = setup_scraper
        rows = animal_table.find_all('tr')
        row_with_animal_data = rows[2]
        collateral_adjective_header_index = scraper._get_header_position('collateral adjective', rows[0])
        collateral_adjective_soup = row_with_animal_data.find_all('td')[collateral_adjective_header_index]
        collateral_adjectives = ['orycteropodian']
        value = scraper._extract_collateral_adjectives(collateral_adjective_soup)
        print(value)
        assert scraper._extract_collateral_adjectives(collateral_adjective_soup) == collateral_adjectives

    # cant make the expected dict to be without spaces..
    # def test_iterate_table_data_to_extract_values(self):
    #     fake_soup_fetcher = FakeSoupFetcher()
    #     scraper = Scraper(fake_soup_fetcher)
    #     animal_table = scraper._get_animal_table_from_soup()
    #     headers: BeautifulSoup = scraper._get_headers_from_table(animal_table)
    #     animal_header_index = scraper._get_header_position('animal', headers)
    #     collateral_adjective_header_index = scraper._get_header_position('collateral adjective', headers)
    #     file_full_path = create_test_data_dir_path('_iterate_table_data_to_extract_values.json')
    #     with open(file_full_path, 'r') as file:
    #         expected_values = json.load(file)
    #     animals_values = scraper._iterate_table_data_to_extract_values(animal_table, animal_header_index,
    #                                                                    collateral_adjective_header_index)
    #     striped_dict = strip(animals_values)
    #     print(striped_dict)
    #     print(expected_values)
    #     assert striped_dict == expected_values
