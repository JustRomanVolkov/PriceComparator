from sqlalchemy import select, func
from models.product import Store, Category, Product
from models.database import async_session
from comparator.logger import setup_logger

logger = setup_logger(__name__)


class PriceFetcher:
    """
    Prints a comparison of the prices.

    This method takes a dictionary of category prices, and prints a comparison of the prices.
    It also calculates the difference between the highest and lowest prices, and identifies the store with the lowest price.

    Args:
        category_prices (dict): A dictionary of category prices.

    Returns:
        None
    """
    async def fetch_average_prices(self):
        """
        Prints a comparison of the prices.

        This method takes a dictionary of category prices, and prints a comparison of the prices.
        It also calculates the difference between the highest and lowest prices, and identifies the store with the lowest price.

        Args:
            category_prices (dict): A dictionary of category prices.

        Returns:
            None
        """
        async with async_session() as session:
            stmt = (
                select(
                    Store.name.label('store_name'),
                    Category.name.label('category_name'),
                    func.avg(Product.price_new).label('average_price')
                )
                .join(Product, Store.id == Product.store_id)
                .join(Category, Category.id == Product.category_id)
                .group_by(Store.name, Category.name)
            )
            result = await session.execute(stmt)
            logger.info("Fetched average prices from the database")
            return result.fetchall()

    async def fetch_stores(self):
        """
        Asynchronously fetches the names of all stores from the database.

        This method executes a SQL statement that selects the name of each store.

        Returns:
            list: A list of store names.
        """
        async with async_session() as session:
            stmt = select(Store.name)
            result = await session.execute(stmt)
            stores = [row[0] for row in result.fetchall()]
            logger.info("Fetched stores from the database")
            return stores
