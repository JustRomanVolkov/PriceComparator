from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from config import DATABASE_URL


# Create an asynchronous engine instance associated with the database URL from the config file.
engine = create_async_engine(DATABASE_URL, echo=False)

# Create an asynchronous session maker bound to the engine.
# This session maker will create instances of AsyncSession and will not expire objects when the transaction ends.
async_session = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)

# Create a base class for declarative models.
Base = declarative_base()


# Asynchronous function to initialize the database.
# This function will create all tables defined in the declarative models.
async def init_db():
    # Begin a new transaction.
    async with engine.begin() as conn:
        # Import the models.
        from .product import Store, Category, Product
        # Create all tables in the database.
        await conn.run_sync(Base.metadata.create_all)


# Asynchronous function to clear the database.
# This function will drop all tables and then recreate them.
async def clear_db():
    # Begin a new transaction.
    async with engine.begin() as conn:
        # Drop all tables in the database.
        await conn.run_sync(Base.metadata.drop_all)
