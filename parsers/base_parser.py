from abc import ABC, abstractmethod
import aiohttp
from typing import List, Dict, Any
from bs4 import BeautifulSoup


class BaseParser(ABC):
    """
    Abstract base class for a web parser.

    Attributes:
        base_url (str): The base URL for the website to be parsed.
        section_url (str): The specific section of the website to be parsed.
        soup (BeautifulSoup): BeautifulSoup object that holds the parsed HTML of the current page.
    """

    def __init__(self, base_url: str, section_url: str):
        """
        Initialize the parser with the base and section URLs.

        Args:
            base_url (str): The base URL for the website to be parsed.
            section_url (str): The specific section of the website to be parsed.
        """
        self.base_url = base_url
        self.section_url = section_url
        self.soup = None

    async def fetch_html(self, url: str) -> str:
        """
        Fetch the HTML content of the given URL.

        Args:
            url (str): The URL to fetch the HTML from.

        Returns:
            str: The HTML content of the page. None if there was an error fetching the page.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    response.raise_for_status()
                    html = await response.text()
                    self.soup = BeautifulSoup(html, 'html.parser')
                    return html
        except aiohttp.ClientError as e:
            print(f'Ошибка при запросе URL: {e}')
            return None

    async def get_product_links(self, product_elements: List[Dict[str, str]]) -> List[str]:
        """
        Fetch the HTML content of the given URL.

        Args:
            url (str): The URL to fetch the HTML from.

        Returns:
            str: The HTML content of the page. None if there was an error fetching the page.
        """
        full_url = self.base_url + self.section_url
        html_content = await self.fetch_html(full_url)
        if not html_content:
            return []

        product_links = []
        product_elements_found = self.soup.find_all(*product_elements)
        for element in product_elements_found:
            link = element.get('href')
            if link:
                link = link.lstrip('/')
                full_link = self.base_url + link
                product_links.append(full_link)

        return product_links[:3]

    async def get_product_details(self, product_url: str, details_elements: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get the details of a specific product.

        Args:
            product_url (str): The URL of the product.
            details_elements (Dict[str, Any]): Dictionary of HTML elements to search for product details.

        Returns:
            Dict[str, Any]: Dictionary of product details. None if there was an error fetching the page.
        """
        html_content = await self.fetch_html(product_url)
        if not html_content:
            return None

        product_details = {}
        for detail, element in details_elements.items():
            detail_element = self.soup.find(*element)
            product_details[detail] = detail_element.get_text(strip=True) if detail_element else f'{detail.capitalize()} не найдено'

        return product_details

    @abstractmethod
    async def parse_product_links(self) -> List[str]:
        """
        Abstract method to parse product links.

        This method should be implemented by any class that inherits from BaseParser.

        Returns:
            List[str]: List of product links.
        """
        pass

    @abstractmethod
    async def parse_product_details(self, product_url: str) -> Dict[str, Any]:
        """
        Abstract method to parse product details.

        This method should be implemented by any class that inherits from BaseParser.

        Args:
            product_url (str): The URL of the product.

        Returns:
            Dict[str, Any]: Dictionary of product details.
        """
        pass
