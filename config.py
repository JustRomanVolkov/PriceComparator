from dotenv import load_dotenv
import os

load_dotenv()

MAGNIT_BASE_URL = os.getenv('MAGNIT_BASE_URL', 'https://dostavka.magnit.ru')
PEREKRESTOK_BASE_URL = os.getenv('PEREKRESTOK_BASE_URL', 'https://www.perekrestok.ru')

DATABASE_URL=os.getenv('DATABASE_URL', 'postgresql+asyncpg://username:password@localhost:5432/price_compare')

# Укажите свои магазины и разделы
STORES = {
    "Магнит": MAGNIT_BASE_URL,
    "Перекрёсток": PEREKRESTOK_BASE_URL,
}

SECTIONS = {
    "Готовая еда": {
        "Магнит": "express/catalog/4435-gotovaya-yeda",
        "Перекрёсток": "cat/mc/25/gotovaa-eda"
    },
    "Кофе": {
        "Магнит": "express/catalog/44121-kofe",
        "Перекрёсток": "cat/c/80/kofe"
    },
    "Молоко": {
        "Магнит": "express/catalog/45723-moloko-pasterizovannoye",
        "Перекрёсток": "cat/c/114/moloko"
    }
}
