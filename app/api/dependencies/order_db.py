import json
from typing import Optional


class JSONOrderDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def read_db(self):
        try:
            with open(self.db_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def write_db(self, data):
        with open(self.db_path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_order_by_id(self, order_id: int) -> Optional[dict]:
        orders = self.read_db()
        for order in orders:
            if order['order_id'] == order_id:
                return order
        return None

    def create_order(self, order: dict) -> dict:
        orders = self.read_db()
        order_dict = order.to_dict()
        orders.append(order_dict)
        self.write_db(orders)
        return order

    def update_order(self, order_id: int, new_order_data: dict) -> Optional[dict]:
        orders = self.read_db()
        for index, order in enumerate(orders):
            if order['order_id'] == order_id:
                orders[index].update(new_order_data)
                self.write_db(orders)
                return orders[index]
        return None

    def delete_order(self, order_id: int) -> bool:
        orders = self.read_db()
        initial_length = len(orders)
        orders = [order for order in orders if order['order_id'] != order_id]
        self.write_db(orders)
        return len(orders) < initial_length

    def create_order_item(self, order_id: int, order_item: dict) -> Optional[dict]:
        orders = self.read_db()
        for index, order in enumerate(orders):
            if order['order_id'] == order_id:
                orders[index]['order_items'].append(order_item)
                self.write_db(orders)
                return orders[index]
        return None

    def get_orders_by_date(self, order_date: str) -> list:
        orders = self.read_db()
        return [order for order in orders if order['order_date'] == order_date]