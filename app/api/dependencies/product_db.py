import json
from typing import Optional


class JSONProductDatabase:
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

    def get_product_by_id(self, product_id: int) -> Optional[dict]:
        products = self.read_db()
        for product in products:
            if product['id'] == product_id:
                return product
        return None

    def create_product(self, product: dict) -> dict:
        products = self.read_db()
        product_dict = product.to_dict()
        products.append(product_dict)
        self.write_db(products)
        return product

    def update_product(self, product_id: int, new_product_data: dict) -> Optional[dict]:
        products = self.read_db()
        for index, product in enumerate(products):
            if product['id'] == product_id:
                products[index].update(new_product_data)
                self.write_db(products)
                return products[index]
        return None

    def delete_product(self, product_id: int) -> bool:
        products = self.read_db()
        initial_length = len(products)
        products = [product for product in products if product['id'] != product_id]
        self.write_db(products)
        return len(products) < initial_length