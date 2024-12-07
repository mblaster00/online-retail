from flask import render_template
from app.config import app
from flask import url_for

# Routes
@app.route('/')
def index():
    list_items = []
    return render_template("index.html")

@app.route('/shopping-history/<customer_id>')
def shopping_cart(customer_id):
    list_products = []
    return render_template("shopping-cart.html")

@app.route('/product/<product_id>')
def product(product_id):
    return render_template("product-page.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")