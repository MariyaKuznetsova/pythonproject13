import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY

def create_stripe_product(name, description):
    """Создание продукта"""

    product = stripe.Product.create(name=name, description=description)

    return product

def create_stripe_price(product, sum_payment):
    """Создание цены"""

    price = stripe.Price.create(
        currency="rub",
        unit_amount=sum_payment * 100,
        product=product.get('id'),
    )

    return price


def create_stripe_session(price):
    """Создание сессии на оплату."""

    session = stripe.checkout.Session.create(
        success_url="http://127.0.0.1:8000/study/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")