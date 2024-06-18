from .common_parser import CommonParser
from .selectors import magnit_selectors, perekrestok_selectors


# The ParserFactory class is responsible for creating and returning an instance of the CommonParser class.
# It uses the store_name parameter to determine which selectors to use when creating the CommonParser instance.
class ParserFactory:
    # The create_parser method is a static method that takes three parameters: store_name, base_url, and section_url.
    # It returns an instance of the CommonParser class.
    @staticmethod
    def create_parser(store_name: str, base_url: str, section_url: str) -> CommonParser:
        # If the store_name is "Магнит", it creates a CommonParser instance with the magnit_selectors.
        if store_name == "Магнит":
            return CommonParser(base_url, section_url, magnit_selectors)
        # If the store_name is "Перекрёсток", it creates a CommonParser instance with the perekrestok_selectors.
        elif store_name == "Перекрёсток":
            return CommonParser(base_url, section_url, perekrestok_selectors)
        # If the store_name is neither "Магнит" nor "Перекрёсток", it raises a ValueError.
        else:
            raise ValueError(f"Неизвестный магазин: {store_name}")
