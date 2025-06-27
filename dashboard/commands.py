import click
from flask.cli import with_appcontext
from .extensions import db
from .models import Customer, Product, Order
from random import randint, choice
from faker import Faker
from sqlalchemy.sql import func

@click.command(name='create_tables')
@with_appcontext
def create_tables():
    db.create_all()

@click.command(name='create_products')
@with_appcontext
def create_products():
    products = [
        Product(name='Product A', price=100.0, monthly_goal=10000.0),
        Product(name='Product B', price=200.0, monthly_goal=20000.0),
        Product(name='Product C', price=300.0, monthly_goal=30000.0)
    ]
    db.session.add_all(products)
    db.session.commit()

@click.command(name='create_orders')
@with_appcontext
def create_orders():
    products = Product.query.all()

    for _ in range(10):
        customer = Customer(name=Faker().name())
        db.session.add(customer)
        db.session.flush()  # Ensure customer is added before creating orders
        order = Order(
            customer_id=customer.id,
            product_id=choice(products).id,
            quantity=randint(1, 7),
            date=Faker().date_time_between(start_date='-600d', end_date='now'),
        )
        db.session.add(order)
    db.session.commit()




