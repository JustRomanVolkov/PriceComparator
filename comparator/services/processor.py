from comparator.logger import setup_logger

logger = setup_logger(__name__)


class ResultProcessor:
    """
    The ResultProcessor class is responsible for processing the results fetched from the PriceFetcher.

    This class has a single static method, process_results, which takes a list of results and processes them into a dictionary.
    The dictionary is structured such that each category is a key, and the value is another dictionary where each store is a key and the average price is the value.
    """
    @staticmethod
    def process_results(results):
        """
        Process the fetched results into a dictionary.

        This method takes a list of results and processes them into a dictionary.
        The dictionary is structured such that each category is a key, and the value is another dictionary where each store is a key and the average price is the value.

        Args:
            results (list): A list of results fetched from the PriceFetcher.

        Returns:
            dict: A dictionary where each category is a key, and the value is another dictionary where each store is a key and the average price is the value.
        """
        category_prices = {}
        for result in results:
            category = result.category_name
            store = result.store_name
            average_price = round(result.average_price, 2)

            if category not in category_prices:
                category_prices[category] = {}
            category_prices[category][store] = average_price
        logger.info("Processed results into category prices")
        return category_prices
