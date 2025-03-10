from flask import render_template, request, redirect, url_for, flash, session
from sqlalchemy import func
from app.config import app
from app.model import db, Customer, Buy, Item
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import pickle
import numpy as np
from datetime import datetime

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Load the RFM model
def load_rfm_model():
    with open('rfm_model.pkl', 'rb') as file:
        return pickle.load(file)

rfm_model = load_rfm_model()

@app.context_processor
def inject_cart_count():
    if current_user.is_authenticated:
        # Count distinct items bought by the customer
        item_count = db.session.query(func.count(Buy.itemId.distinct())) \
            .filter(Buy.customerId == current_user.customerId) \
            .scalar()
    else:
        item_count = 0
    return dict(cart_count=item_count)

# Customize the login redirection
@login_manager.unauthorized_handler
def unauthorized():
    flash('Please log in to view this product.', 'error')
    return redirect(url_for('login', next=request.url))

@login_manager.user_loader
def load_user(user_id):
    return Customer.query.get(int(user_id))

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'success')
    return redirect(url_for('index'))

@app.route('/')
def index():
    try:
        # Get all items from database
        items = Item.query.all()
        return render_template("index.html", items=items)
    except Exception as e:
        print(f"Error: {e}")  # For debugging
        # Return empty list if there's an error
        return render_template("index.html", items=[])

@app.route('/register', methods=['GET', 'POST'])
def register():
    # If user is already logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        # Get form data
        username = request.form.get('username')
        password = request.form.get('password')
        country = request.form.get('country')
        city = request.form.get('city')
        address = request.form.get('address')
        zipcode = request.form.get('zipcode')

        # Validate required fields
        if not all([username, password, country, city, address, zipcode]):
            flash('All fields are required!', 'error')
            return redirect(url_for('register'))

        # Check if username already exists
        if Customer.query.filter_by(username=username).first():
            flash('Username already exists!', 'error')
            return redirect(url_for('register'))

        try:
            # Create new customer
            new_customer = Customer(
                username=username,
                country=country,
                city=city,
                address=address,
                zipcode=zipcode,
                customer_segment='New',
                segment_description='Not enough purchase history.',
                recommended_strategy='Welcome offers, introductory promotions'
            )
            new_customer.set_password(password)

            # Add to database
            db.session.add(new_customer)
            db.session.commit()

            # Success message and redirect to login
            flash('Registration successful! Please login to continue.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            flash('An error occurred during registration.', 'error')
            return redirect(url_for('register'))

    # GET request - show the registration form
    return render_template("register.html")
@app.route('/login', methods=['GET', 'POST'])
def login():
    # If user is already logged in, redirect to home
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        if not username or not password:
            flash('Please fill in all fields', 'error')
            return redirect(url_for('login'))

        # Find the customer
        customer = Customer.query.filter_by(username=username).first()

        # Check if customer exists and password is correct
        if customer and customer.check_password(password):
            # Log in the user
            login_user(customer)
            flash('Login successful! Welcome back!', 'success')

            # Redirect to home page
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    # GET request - show the login form
    return render_template('login.html')

@app.route('/buy/<int:item_id>', methods=['POST'])
@login_required
def buy_item(item_id):
    try:
        item = Item.query.get_or_404(item_id)
        quantity = int(request.form.get('quantity', 1))

        # Create new purchase
        purchase = Buy(
            customerId=current_user.customerId,
            itemId=item_id,
            quantity=quantity,
            unit_price=item.unit_price,
            invoiceDate=datetime.utcnow()
        )

        db.session.add(purchase)

        # Update customer's metrics
        current_user.calculate_rfm_metrics()

        db.session.commit()
        flash('Purchase successful!', 'success')
        return redirect(url_for('shopping_cart', customer_id=current_user.customerId))

    except Exception as e:
        db.session.rollback()
        flash('Error processing your purchase. Please try again.', 'error')
        return redirect(url_for('product', product_id=item_id))


@app.route('/shopping-history/<int:customer_id>')
@login_required
def shopping_cart(customer_id):
    if current_user.customerId != customer_id:
        flash('Unauthorized access', 'error')
        return redirect(url_for('index'))

    purchases = Buy.query.filter_by(customerId=customer_id).all()

    # Calculate recency
    recency = None
    if purchases:
        last_purchase = max(purchases, key=lambda x: x.invoiceDate)
        recency = (datetime.utcnow() - last_purchase.invoiceDate).days

    return render_template("shopping-cart.html",
                           purchases=purchases,
                           recency=recency,
                           now=datetime.utcnow())



def update_customer_segment(customer_id):
    customer = Customer.query.get(customer_id)
    if customer:
        # Calculate RFM metrics
        customer.calculate_rfm_metrics()

        # Prepare data for the model
        features = np.array([[
            customer.log_recency,
            customer.log_frequency,
            customer.log_monetary
        ]])

        # Make prediction only if customer has made purchases
        if customer.frequency > 0:
            cluster = rfm_model.predict(features)[0]

            # Map cluster number to detailed segment information
            segments = {
                0: {
                    'name': 'High-Value',
                    'description': 'Recent purchases, frequent buyer, high spender.',
                    'strategy': 'VIP treatment, early access to new products, exclusive offers'
                },
                1: {
                    'name': 'Moderate-Value',
                    'description': 'Regular customer with moderate spending.',
                    'strategy': 'Targeted promotions to increase purchase frequency'
                },
                2: {
                    'name': 'Low-Engagement',
                    'description': 'Infrequent purchases, low spending.',
                    'strategy': 'Re-engagement campaigns, special discounts'
                },
                3: {
                    'name': 'Inactive-Valuable',
                    'description': 'Previously valuable, currently inactive.',
                    'strategy': 'Reactivation campaigns, personalized offers'
                },
                4: {
                    'name': 'Churned-Moderate',
                    'description': 'Previously moderate value, now inactive.',
                    'strategy': 'Win-back campaigns, loyalty rewards'
                }
            }

            segment_info = segments.get(cluster, {
                'name': 'New',
                'description': 'Not enough purchase history.',
                'strategy': 'Welcome offers, introductory promotions'
            })

            # Update customer information
            customer.customer_segment = segment_info['name']
            customer.segment_description = segment_info['description']
            customer.recommended_strategy = segment_info['strategy']

            db.session.commit()

@app.route('/product/<product_id>')
@login_required  # This decorator ensures user must be logged in
def product(product_id):
    item = Item.query.get_or_404(product_id)
    return render_template("product-page.html", item=item)