from app.api.dependencies.order_db import JSONOrderDatabase
from app.models.order import Order

class OrderService:
    def __init__(self, db_path):
        self.db = JSONOrderDatabase(db_path)

    def get_all_orders(self):
        return self.db.read_db()

    def get_order_by_id(self, order_id):
        return self.db.get_order_by_id(order_id)