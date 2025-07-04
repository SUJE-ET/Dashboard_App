from .extensions import db
from datetime import datetime
from sqlalchemy.sql import func
from flask_login import UserMixin
from werkzeug.security import generate_password_hash

class Customer(db.Model):
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    orders = db.relationship("Order", backref="customer", lazy=True)

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    price = db.Column(db.Float)
    monthly_goal = db.Column(db.Float)
    orders = db.relationship("Order", backref="product", lazy=True)

    def revenue_this_month(self):
        first_of_month = datetime.today().replace(
            day=1, hour=0, minute=0, second=0, microsecond=0
        )
        return db.session.query(func.sum(Order.quantity*self.price)).filter(Order.product_id == self.id, Order.date>first_of_month).scalar() or 0
    

class Order(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    quantity = db.Column(db.Integer, nullable=False)
    date = db.Column(db.DateTime)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'))

    @staticmethod
    def get_monthly_earnings():
        monthly_earnings = db.session.query(
        func.extract('year', Order.date),
        func.extract('month', Order.date),
        func.sum(Order.quantity* Product.price),
        func.count()
        ).join(Product).group_by(
            func.extract('year',Order.date),
            func.extract('month', Order.date)
            ).all()
        return monthly_earnings
    
    @staticmethod
    def get_revenue_per_product():
        revenue_per_product = db.session.query(
        Product.name,
        func.sum(Order.quantity*Product.price)
        ).join(Product).group_by(Product.id).all()
        return revenue_per_product
    
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(50))
    email_address  = db.Column(db.String(50))
    password_hash = db.Column(db.String(50))

    @property
    def password(self):
        raise AttributeError('Cannot view password')

    @password.setter
    def password(self, password):
        self.password_hash= generate_password_hash(password)

    
