from app.models.order import Order, OrderItem
from app.api.dependencies.order_db import JSONOrderDatabase

db = JSONOrderDatabase('db_orders.json')

class CRUDOrder:
    @staticmethod
    def get_order_by_id(id: int) -> Order:
        return db.get_order_by_id(id)

    @staticmethod
    def get_all_orders() -> list:
        return db.read_db()

    @staticmethod
    def create_order(order: Order) -> Order:
        order_data = order.to_dict()
        order_data['order_id'] = db.read_db()[-1]['order_id'] + 1 if db.read_db() else 1

        return db.create_order(Order(**order_data))

    @staticmethod
    def update_order(id: int, order: Order) -> Order:
        return db.update_order(id, order)

    @staticmethod
    def delete_order(id: int) -> None:
        db.delete_order(id)

    @staticmethod
    def create_order_item(order_id: int, order_item: OrderItem) -> Order:
        return db.create_order_item(order_id, order_item)

    @staticmethod
    def get_orders_by_date(order_date: str) -> list:
        return db.get_orders_by_date(order_date)