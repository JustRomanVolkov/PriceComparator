magnit_selectors = {
    'product_links': ('a', {'class': 'app-link product-card product-list__item'}),
    'product_details': {
        'name': ('h1', {'class': 'm-page-header__title text--h1'}),
        'description': ('div', {'class': 'product-detail-text'}),
        'price_new': ('div', {'data-test-id': 'product-price'}),
        'price_old': ('div', {'data-test-id': 'product-price_old'}),
        'article': ('span', {'data-test-id': 'product-article'}),
    }
}

perekrestok_selectors = {
    'product_links': ('a', {'class': 'product-card__link'}),
    'product_details': {
        'name': ('h1', {'class': 'sc-fubCzh ibFUIH product__title'}),
        'price_new': ('div', {'class': 'price-new'}),
        'price_old': ('div', {'class': 'price-old'}),
        'rating': ('div', {'role': 'img', 'class': 'sc-fFucqa drDzyo'}),
        'availability': ('div', {'class': 'price-card-balance-state'}),
    }
}
