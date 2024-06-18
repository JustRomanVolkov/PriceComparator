from .base_parser import BaseParser
from utils.data_cleaner import clean_price, clean_rating
from typing import List, Dict, Any


class CommonParser(BaseParser):
    """
    A parser that extends the BaseParser for common parsing tasks.

    Attributes:
        selectors (Dict[str, Any]): A dictionary of selectors used for parsing.
    """
    def __init__(self, base_url: str, section_url: str, selectors: Dict[str, Any]):
        """
        Initialize the parser with the base and section URLs and selectors.

        Args:
            base_url (str): The base URL for the website to be parsed.
            section_url (str): The specific section of the website to be parsed.
            selectors (Dict[str, Any]): A dictionary of selectors used for parsing.
        """
        super().__init__(base_url, section_url)
        self.selectors = selectors

    async def parse_product_links(self) -> List[str]:
        """
        Parse product links using the 'product_links' selector.

        Returns:
            List[str]: List of product links.
        """
        return await self.get_product_links(self.selectors['product_links'])

    async def parse_product_details(self, product_url: str) -> Dict[str, Any]:
        """
        Parse product details using the 'product_details' selector and clean the data.

        Args:
            product_url (str): The URL of the product.

        Returns:
            Dict[str, Any]: Dictionary of cleaned product details.
        """
        product_details = await self.get_product_details(product_url, self.selectors['product_details'])
        if product_details:
            if 'price_new' in product_details:
                product_details['price_new'] = clean_price(product_details['price_new'])
            if 'price_old' in product_details:
                product_details['price_old'] = clean_price(product_details['price_old'])
            if 'rating' in product_details:
                product_details['rating'] = clean_rating(product_details['rating'])
        return product_details
