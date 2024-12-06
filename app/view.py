from flask import render_template
from app.config import app
from flask import url_for

# Routes
@app.route('/')
def index():
    list_items = []
    return render_template("index.html")

@app.route('/shopping-cart')
def shopping_cart():
    list_products = []
    return render_template("index.html")

@app.route('/product-id')
def product():
    return render_template("index.html")

@app.route('/login')
def login():
    return render_template("login.html")

@app.route('/register')
def register():
    return render_template("register.html")