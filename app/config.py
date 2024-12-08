import os
from flask import Flask

UPLOAD_FOLDER = "app/static/imagesdata/"
UPLOAD_FOLDER2 = "app/"

app_root = os.path.dirname(os.path.abspath(__file__))
# UPLOAD_FOLDER = os.path.join(app_root, 'app', 'static', 'imagesdata')

# Configurations
app = Flask(__name__)
# app.config.from_object('config')

# MySQL configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:Vegeta#5@localhost/online_retail'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Secret key for session management
app.config['SECRET_KEY'] = 'Vegeta#5'