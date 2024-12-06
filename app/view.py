from flask import render_template
from app.config import app
from flask import url_for

# Routes
@app.route('/')
def index():
    list_products = []
    return render_template("index.html")

@app.route('/shopping-cart')
def shopping_cart():
    list_products = []
    return render_template("index.html")

@app.route('/product-id')
def product():
    list_products = []
    return render_template("index.html")

@app.route('/login')
def login():
    list_products = []
    return render_template("login.html")

@app.route('/register')
def register():
    list_products = []
    return render_template("register.html")