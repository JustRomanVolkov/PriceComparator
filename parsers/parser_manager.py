import asyncio
from config import STORES, SECTIONS
from parsers.parser_factory import ParserFactory
from models.database import async_session
from models.product import Store, Category, Product
from sqlalchemy.future import select
from sqlalchemy.exc import IntegrityError
from contextlib import asynccontextmanager


class ParserManager:
    """
    The ParserManager class is responsible for managing the parsing process.
    It includes methods for creating sessions, getting or creating instances of models,
    processing individual products, processing all products for a given store and category,
    and running the entire parsing process.
    """

    @asynccontextmanager
    async def get_session(self):
        """
        Asynchronous context manager for getting a session.
        Yields a session from the async_session.
        """
        async with async_session() as session:
            yield session

    async def get_or_create(self, session, model, name: str):
        """
        Asynchronous method to get or create an instance of a model.
        If the instance does not exist, it is created and added to the session.
        If an IntegrityError occurs during the creation, the session is rolled back and the instance is retrieved again.

        Args:
            session: The session to use for database operations.
            model: The model class of the instance to get or create.
            name: The name of the instance to get or create.

        Returns:
            The instance that was gotten or created.
        """
        result = await session.execute(select(model).filter(model.name == name))
        instance = result.scalars().first()
        if not instance:
            instance = model(name=name)
            try:
                session.add(instance)
                await session.commit()
                await session.refresh(instance)
            except IntegrityError:
                await session.rollback()
                result = await session.execute(select(model).filter(model.name == name))
                instance = result.scalars().first()
        return instance

    async def process_product(self, store_id, category_id, parser, product_url, semaphore):
        """
        Asynchronous method to process a single product.
        The product details are parsed and then added to the session.
        If an error occurs during this process, the session is rolled back.

        Args:
            store_id: The ID of the store the product belongs to.
            category_id: The ID of the category the product belongs to.
            parser: The parser to use for parsing the product details.
            product_url: The URL of the product to parse.
            semaphore: The semaphore to use for limiting the number of concurrent tasks.
        """
        async with semaphore:
            product_details = await parser.parse_product_details(product_url)
            if product_details:
                product_details['store_id'] = store_id
                product_details['category_id'] = category_id
                async with self.get_session() as session:
                    try:
                        product = Product(**product_details)
                        session.add(product)
                        await session.commit()
                        print(f"Товар {product_details['name']} сохранен.")
                    except Exception as e:
                        print(f"Ошибка при сохранении товара: {e}")
                        await session.rollback()
                print(f'Товар:')
                for key, value in product_details.items():
                    print(f'{key.capitalize()}: {value}')
                print('---')
            else:
                print(f'Не удалось получить данные для товара: {product_url}')

    async def process_products(self, store_name, base_url, section_url, category_name):
        """
        Asynchronous method to process all products for a given store and category.
        A parser is created for the store and category, and then all product links are parsed and processed.

        Args:
            store_name: The name of the store to process products for.
            base_url: The base URL of the store.
            section_url: The URL of the section to process products for.
            category_name: The name of the category to process products for.
        """
        parser = ParserFactory.create_parser(store_name, base_url, section_url)
        async with self.get_session() as session:
            store = await self.get_or_create(session, Store, store_name)
            category = await self.get_or_create(session, Category, category_name)
            store_id = store.id
            category_id = category.id

        product_links = await parser.parse_product_links()
        semaphore = asyncio.Semaphore(10)
        tasks = [self.process_product(store_id, category_id, parser, product_url, semaphore) for product_url in product_links]
        await asyncio.gather(*tasks)

    async def run(self):
        """
        Asynchronous method to run the entire parsing process.
        For each category and store, a task is created to process all products.
        All tasks are then run concurrently.
        """
        tasks = []
        for category_name, section_values in SECTIONS.items():
            for store_name, base_url in STORES.items():
                task = self.process_products(
                    store_name,
                    base_url,
                    section_values[store_name],
                    category_name
                )
                tasks.append(task)
        await asyncio.gather(*tasks)
