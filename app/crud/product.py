from app.models.product import Product
from app.api.dependencies.product_db import JSONProductDatabase

db = JSONProductDatabase('db_product.json')

class CRUDProduct:
    @staticmethod
    def get_product_by_id(id: int) -> Product:
        return db.get_product_by_id(id)

    @staticmethod
    def get_all_products() -> list:
        return db.read_db()

    @staticmethod
    def create_product(product: Product) -> Product:
        product_data = product.to_dict()
        product_data['id'] = db.read_db()[-1]['id'] + 1 if db.read_db() else 1

        return db.create_product(Product(**product_data))

    @staticmethod
    def update_product(id: int, product: Product) -> Product:
        return db.update_product(id, product)

    @staticmethod
    def delete_product(id: int) -> None:
        db.delete_product(id)