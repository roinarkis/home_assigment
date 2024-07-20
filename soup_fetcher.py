from bs4 import BeautifulSoup
import requests
from abc import abstractmethod, ABC


class AbstractSoupFetcher(ABC):
    @abstractmethod
    def get_soup(self):
        raise NotImplemented


class SoupFetcher(AbstractSoupFetcher):
    def __init__(self, base_url: str):
        self.base_url: str = base_url

    def get_soup(self) -> BeautifulSoup:
        try:
            session = requests.Session()
            response = session.get(self.base_url)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            return soup
        except requests.exceptions.RequestException as e:
            print(f"Failed to retrieve page : {e}")
