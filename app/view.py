from flask import render_template
from app.config import app
from flask import url_for

# Routes
@app.route('/')
def index():
    list_products = []
    return render_template("index.html")

@app.route('/shopping-cart')
def index():
    list_products = []
    return render_template("index.html")

@app.route('/product-id')
def index():
    list_products = []
    return render_template("index.html")

@app.route('/login')
def index():
    list_products = []
    return render_template("login.html")

@app.route('/register')
def index():
    list_products = []
    return render_template("register.html")