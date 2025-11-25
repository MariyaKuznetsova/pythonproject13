import stripe
from config.settings import STRIPE_API_KEY


stripe.api_key = STRIPE_API_KEY

def create_stripe_products(name, description):
    """Создание продукта"""

    product = stripe.Product.create(name="name", description="description")

    return product

def create_stripe_price(sum_payment):
    """Создание цены"""

    price = stripe.Price.create(
        currency="rub",
        unit_amount=sum_payment * 100,
        product_data={"name": "Payment"},
    )

    return price


def create_stripe_session():
    """Создание сессии на оплату."""
    session = stripe.checkout.Session.create(
        success_url="https://127.0.0.1:8000/",
        line_items=[{"price": price.get("id"), "quantity": 1}],
        mode="payment",
    )

    return session.get("id"), session.get("url")