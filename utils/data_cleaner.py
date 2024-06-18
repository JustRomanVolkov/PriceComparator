# utils/data_cleaner.py

def clean_price(price_text: str) -> float:
    try:
        return float(''.join(char for char in price_text if char.isdigit() or char == ',').replace(',', '.'))
    except ValueError:
        return 0.0


def clean_rating(rating_text: str) -> float | None:
    try:
        return float(rating_text.replace(',', '.')) if rating_text else None
    except ValueError:
        return None
