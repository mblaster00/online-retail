from app.config import app
from app.model import db, Item, Buy
from datetime import datetime

from app.view import app
from app.model import db

if __name__ == '__main__':
    # with app.app_context():
        # db.create_all()
        # insert_data()
    app.run(debug=True)

# def insert_data():
#     items_data = [
#         {
#             'item': {
#                 'stockCode': '85123A',
#                 'description': 'WHITE HANGING HEART T-LIGHT HOLDER',
#                 'unit_price': 2.55
#             },
#             'purchase': {
#                 'invoiceNo': '536365',
#                 'customerId': 1,
#                 'quantity': 6
#             }
#         },
#         {
#             'item': {
#                 'stockCode': '71053',
#                 'description': 'WHITE METAL LANTERN',
#                 'unit_price': 3.39
#             },
#             'purchase': {
#                 'invoiceNo': '536365',
#                 'customerId': 1,
#                 'quantity': 6
#             }
#         },
#         # Add other items...
#     ]
#
#     with app.app_context():
#         for data in items_data:
#             # First, check if item already exists
#             item = Item.query.filter_by(stockCode=data['item']['stockCode']).first()
#
#             if not item:
#                 # Create new item
#                 item = Item(**data['item'])
#                 db.session.add(item)
#                 db.session.flush()  # This gets us the item ID
#
#             # Create purchase record
#             purchase = Buy(
#                 itemId=item.itemId,
#                 invoiceNo=data['purchase']['invoiceNo'],
#                 customerId=data['purchase']['customerId'],
#                 quantity=data['purchase']['quantity'],
#                 unit_price=item.unit_price,
#                 invoiceDate=datetime.utcnow()
#             )
#             db.session.add(purchase)
#
#         try:
#             db.session.commit()
#             print("Data inserted successfully!")
#         except Exception as e:
#             db.session.rollback()
#             print(f"Error inserting data: {str(e)}")
#
#
