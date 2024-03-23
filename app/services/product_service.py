from app.api.dependencies.product_db import JSONProductDatabase

db = JSONProductDatabase('db_products.json')


class ProductService:
    @staticmethod
    def get_all_products():
        return db.read_db()

    @staticmethod
    def get_product_by_id(product_id: int):
        return db.get_product_by_id(product_id)

    @staticmethod
    def create_product(product: dict):
        return db.create_product(product)

    @staticmethod
    def update_product(product_id: int, new_product_data: dict):
        return db.update_product(product_id, new_product_data)

    @staticmethod
    def delete_product(product_id: int):
        return db.delete_product(product_id)

