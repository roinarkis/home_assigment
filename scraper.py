import bs4.element
from soup_fetcher import  AbstractSoupFetcher
from constants import TABLE_CLASS_NAME
from exceptions import ClassNameNotFound, URlNotFound
from bs4 import BeautifulSoup
from dtos.animal import Animal
from pictures_handler import PictureHandler


class Scraper:

    def __init__(self, soup_fetcher: AbstractSoupFetcher):
        self._soup_fetcher = soup_fetcher

    def _get_animal_table_from_soup(self) -> BeautifulSoup:
        soup: BeautifulSoup = self._soup_fetcher.get_soup()
        if soup is None:
            raise URlNotFound('Could not find URL')
        animal_table:BeautifulSoup = soup.find(class_=TABLE_CLASS_NAME)
        if animal_table is None:
            raise ClassNameNotFound('Could not find animal table from HTML')

        return animal_table

    @classmethod
    def _get_header_position(cls, header_to_find: str, headers_soup: bs4.element.Tag) -> int:
        header_position = None
        headers:bs4.element.ResultSet = headers_soup.find_all('th')
        for header in headers:
            header_a_tag = header.find('a')
            if header_a_tag:
                if header_to_find in header_a_tag.text.lower():
                    header_position = headers.index(header)
                    break
            if header_to_find in header.text.lower():
                header_position = headers.index(header)
                break
        return header_position

    @classmethod
    def _row_not_containing_animal_data(cls, row: bs4.element.Tag) -> bool:
        num_of_values = len(row.find_all('td'))
        return num_of_values == 0

    @classmethod
    def _extract_collateral_adjectives(cls, td_element):
        collateral_adjectives = []
        for item in td_element.contents:
            if item.name == 'br' or item.name == 'sup':
                continue
            collateral_adjectives.append(item)
        return collateral_adjectives



    @classmethod
    def _iterate_table_data_to_extract_values(cls, animal_table:BeautifulSoup, animal_name_index:int, collateral_adjective_index:int) -> list[Animal]:
        PictureHandler.create_pictures_folder()
        rows:bs4.element.ResultSet = animal_table.find_all('tr')
        animals = []
        for row in rows:
            if cls._row_not_containing_animal_data(row):
                continue
            try:
                animal_td = row.find_all('td')[animal_name_index]
                animal_name = animal_td.find('a').text
                animal_name_for_url = animal_td.find('a').get('title').replace(' ', '_')
                animal_image_src = PictureHandler.get_picture(animal_name_for_url)
            except (IndexError, AttributeError) as e:
                if isinstance(e, IndexError):
                    print(f'Index Error occurred in getting animal name from table row:{row}')
                else:
                    print(f'AttributeError occurred in the <a> tag inside the animal td in row:{row}')
                continue

            try:
                collateral_adjective_td = row.find_all('td')[collateral_adjective_index]
                if collateral_adjective_td.find('sup'):
                    animal_collateral_adjective = cls._extract_collateral_adjectives(collateral_adjective_td)
                else:
                    animal_collateral_adjective = collateral_adjective_td.get_text(separator="\n").strip().split("\n")
            except IndexError:
                print(f'Index Error occurred in getting collateral adjective from table in row: {row}')
                continue
            animals.append(
                Animal(name=animal_name, name_for_url=animal_name_for_url, image_src=animal_image_src, collateral_adjectives=animal_collateral_adjective))

        return animals

    @classmethod
    def _get_headers_from_table(cls, animal_table: BeautifulSoup) -> BeautifulSoup:
        rows = animal_table.find_all('tr')
        headers = rows[0]
        return headers


    @classmethod
    def _get_animal_name_and_collateral_adjectives(cls, animal_table: BeautifulSoup) -> list[Animal]:
        headers = cls._get_headers_from_table(animal_table)
        animal_name_index = cls._get_header_position('animal', headers)
        collateral_adjective_index = cls._get_header_position('collateral adjective', headers)
        animals = cls._iterate_table_data_to_extract_values(animal_table, animal_name_index, collateral_adjective_index)
        return animals

    def get_animal_table_values(self) -> list:
        animal_table = self._get_animal_table_from_soup()
        animals = self._get_animal_name_and_collateral_adjectives(animal_table)
        return animals

