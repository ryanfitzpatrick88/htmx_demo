from enum import Enum

from pydantic import BaseModel


class OrderStatus(str, Enum):
    PENDING = 'Pending'
    SHIPPED = 'Shipped'
    COMPLETED = 'Completed'
    CANCELLED = 'Cancelled'


class OrderItem(BaseModel):
    order_item_id: int
    item_name: str
    item_price: float
    item_quantity: int
    product_id: int
    product_name: str

    def calculate_item_total(self):
        return self.item_price * self.item_quantity

    def to_dict(self):
        return {
            'order_item_id': self.order_item_id,
            'item_name': self.item_name,
            'item_price': self.item_price,
            'item_quantity': self.item_quantity,
            'product_id': self.product_id,
            'product_name': self.product_name
        }


class Order(BaseModel):
    order_id: int
    order_date: str
    customer_id: int
    customer_name: str
    order_total: float
    order_status: OrderStatus = OrderStatus.PENDING
    order_items: list[OrderItem]

    def add_order_item(self, order_item):
        self.order_items.append(order_item)

    def remove_order_item(self, order_item):
        self.order_items.remove(order_item)

    def calculate_order_total(self):
        total = 0
        for order_item in self.order_items:
            total += order_item.calculate_item_total()
        self.order_total = total
        return self.order_total

    def to_dict(self):
        return {
            'order_id': self.order_id,
            'order_status': self.order_status,
            'order_date': self.order_date,
            'customer_id': self.customer_id,
            'customer_name': self.customer_name,
            'order_total': self.order_total,
            'order_items': [order_item.to_dict() for order_item in self.order_items]
        }


