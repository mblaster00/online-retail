from app.view import app
from app.model import db

if __name__ == '__main__':
    # Create all database tables
    with app.app_context():
        db.create_all()

    app.run(debug=True)