#!flask/bin/python
import datetime

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from app.config import app

# Initialize SQLAlchemy
db = SQLAlchemy(app)

class Customer(db.Model):
    __tablename__ = 'customer'
    customerId = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(255))
    typeId = db.Column(db.Integer)
    country = db.Column(db.String(100))
    profileId = db.Column(db.Integer, db.ForeignKey('profile.id'))

    # Relationships
    profile = db.relationship('Profile', backref='customers')
    purchases = db.relationship('Buy', backref='customer', lazy=True)

class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))

class Item(db.Model):
    __tablename__ = 'item'
    itemId = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    description = db.Column(db.Text)

    # Relationship
    purchases = db.relationship('Buy', backref='item', lazy=True)

class Buy(db.Model):
    __tablename__ = 'buy'
    id = db.Column(db.Integer, primary_key=True)
    customerId = db.Column(db.Integer, db.ForeignKey('customer.customerId'))
    itemId = db.Column(db.Integer, db.ForeignKey('item.itemId'))
    quantity = db.Column(db.Integer)
    invoiceDate = db.Column(db.DateTime, default=datetime.utcnow)
    invoiceNo = db.Column(db.String(50))