import asyncio
from services.fetcher import PriceFetcher
from services.processor import ResultProcessor
from services.printer import ResultPrinter
from logger import setup_logger
from exceptions import PriceComparatorError

logger = setup_logger(__name__)


class PriceComparator:
    """
    The PriceComparator class is responsible for fetching, processing, and printing price comparisons.

    Attributes:
        fetcher (PriceFetcher): An instance of the PriceFetcher class.
        processor (ResultProcessor): An instance of the ResultProcessor class.
    """
    def __init__(self):
        self.fetcher = PriceFetcher()
        self.processor = ResultProcessor()

    async def calculate_average_price(self):
        """
        The method to calculate the average price.

        This method fetches the average prices and stores, processes the results, and prints the comparison.
        It handles any exceptions that occur during these operations and logs an error message before re-raising the exception.

        Raises:
            PriceComparatorError: If any error occurs during the operations.
        """
        try:
            results = await self.fetcher.fetch_average_prices()
            stores = await self.fetcher.fetch_stores()
            category_prices = self.processor.process_results(results)
            printer = ResultPrinter(stores)
            printer.print_comparison(category_prices)
        except Exception as e:
            logger.error(f"Ошибка при вычислении средней цены: {e}")
            raise PriceComparatorError(e)


if __name__ == "__main__":
    # Creating an instance of the PriceComparator class and running the calculate_average_price method
    comparator = PriceComparator()
    asyncio.run(comparator.calculate_average_price())
