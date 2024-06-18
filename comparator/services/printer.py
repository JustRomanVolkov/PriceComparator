from comparator.logger import setup_logger

logger = setup_logger(__name__)


class ResultPrinter:
    """
    The ResultPrinter class is responsible for printing the comparison of prices.

    This class takes a list of stores and a dictionary of category prices, and prints a comparison of the prices.
    It also calculates the difference between the highest and lowest prices, and identifies the store with the lowest price.

    Attributes:
        stores (list): A list of stores.

    Methods:
        print_comparison(category_prices): Prints a comparison of the prices.
    """
    def __init__(self, stores):
        self.stores = stores

    def print_comparison(self, category_prices):
        """
        Prints a comparison of the prices.

        This method takes a dictionary of category prices, and prints a comparison of the prices.
        It also calculates the difference between the highest and lowest prices, and identifies the store with the lowest price.

        Args:
            category_prices (dict): A dictionary of category prices.

        Returns:
            None
        """
        for category, prices in category_prices.items():
            print(f'Категория: {category}')
            for store in self.stores:
                if store in prices:
                    print(f'{prices[store]} - средняя цена в "{store}"')
            if all(store in prices for store in self.stores):
                difference = round(abs(max(prices.values()) - min(prices.values())), 2)
                cheaper_store = min(self.stores, key=prices.get)
                print(f'Выгоднее покупать в {cheaper_store} на {difference} руб')
            logger.info(f'Printed comparison for category: {category}')
            print("---")
