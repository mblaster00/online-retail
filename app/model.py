#!flask/bin/python
from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import numpy as np
from app.config import app
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy(app)

class Customer(db.Model, UserMixin):
    # Add this method for Flask-Login
    __tablename__ = 'customer'
    customerId = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    country = db.Column(db.String(100))
    city = db.Column(db.String(100))
    address = db.Column(db.String(255))
    zipcode = db.Column(db.String(20))

    # RFM Metrics
    recency = db.Column(db.Integer, nullable=True)
    frequency = db.Column(db.Integer, nullable=True)
    monetary = db.Column(db.Float, nullable=True)

    # Log transformed metrics
    log_recency = db.Column(db.Float, nullable=True)
    log_frequency = db.Column(db.Float, nullable=True)
    log_monetary = db.Column(db.Float, nullable=True)

    # Segment information
    customer_segment = db.Column(db.String(50))
    segment_description = db.Column(db.Text)
    recommended_strategy = db.Column(db.Text)

    def get_id(self):
        return str(self.customerId)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # Relationships
    purchases = db.relationship('Buy', backref='customer', lazy=True)

    def calculate_rfm_metrics(self, reference_date=None):
        """Calculate RFM metrics for the customer"""
        if reference_date is None:
            reference_date = datetime.now()

        purchases = Buy.query.filter_by(customerId=self.customerId).all()

        if purchases:
            # Recency
            last_purchase_date = max(purchase.invoiceDate for purchase in purchases)
            self.recency = (reference_date - last_purchase_date).days

            # Frequency
            self.frequency = len(purchases)

            # Monetary
            self.monetary = sum(purchase.quantity * purchase.unit_price for purchase in purchases)

            # Log transformations
            self.log_recency = np.log1p(self.recency)
            self.log_frequency = np.log1p(self.frequency)
            self.log_monetary = np.log1p(self.monetary)


class Item(db.Model):
    __tablename__ = 'item'
    itemId = db.Column(db.Integer, primary_key=True)
    stockCode = db.Column(db.String(20))
    description = db.Column(db.Text)
    unit_price = db.Column(db.Float)
    is_new = db.Column(db.Boolean, default=False)
    is_sale = db.Column(db.Boolean, default=False)
    is_popular = db.Column(db.Boolean, default=False)
    purchases = db.relationship('Buy', backref='item', lazy=True)


class Buy(db.Model):
    __tablename__ = 'buy'
    id = db.Column(db.Integer, primary_key=True)
    invoiceNo = db.Column(db.String(50))
    customerId = db.Column(db.Integer, db.ForeignKey('customer.customerId'))
    itemId = db.Column(db.Integer, db.ForeignKey('item.itemId'))
    quantity = db.Column(db.Integer)
    invoiceDate = db.Column(db.DateTime)
    unit_price = db.Column(db.Float)

    @property
    def total_amount(self):
        return self.quantity * self.unit_price
