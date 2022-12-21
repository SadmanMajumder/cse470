from . import db 
from flask_login import UserMixin
from sqlalchemy.sql import func

class Customer(UserMixin, db.Model):
    nid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    user_type = db.Column(db.String(100), default='customer')
    balance = db.Column(db.Integer)
    def get_id(self):
        return (self.email)

class Admin(UserMixin, db.Model):
    nid = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(100))
    user_type = db.Column(db.String(100), default='admin')
    balance = db.Column(db.Integer, default=0)
    def get_id(self):
        return (self.email)
    
class Products(db.Model):
    product_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_name = db.Column(db.String(100))
    product_amount = db.Column(db.Integer)
    product_description = db.Column(db.String(100))
    product_rating = db.Column(db.String(100), default='5')
    product_price = db.Column(db.String(100))

class Payment(db.Model):
    payment_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    payment_amount = db.Column(db.Integer)
    payment_coupon = db.Column(db.String(100))
    
class Coupon(db.Model):
    coupon_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    coupon_name = db.Column(db.String(100))
    coupon_amount = db.Column(db.Integer)
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.Integer)
