import asyncio
from parsers.parser_manager import ParserManager
from models.database import init_db, clear_db


# This is the main function of the program. It initializes the database and runs the parser manager.
async def main():
    # await clear_db()  # This line is commented out. If uncommented, it would clear the database before initialization.
    await init_db()  # This line initializes the database.
    parser_manager = ParserManager()  # This line creates an instance of the ParserManager class.
    await parser_manager.run()  # This line runs the parser manager.


if __name__ == "__main__":
    asyncio.run(main())
