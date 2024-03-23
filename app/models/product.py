from pydantic import BaseModel
from typing import Optional
from enum import Enum


class Category(str, Enum):
    electronics = "electronics"
    clothing = "clothing"
    shoes = "shoes"
    books = "books"
    home = "home"
    sports = "sports"
    outdoors = "outdoors"
    toys = "toys"
    beauty = "beauty"
    health = "health"
    food = "food"
    other = "other"


class Product(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category: Category
    brand: str
    color: Optional[str] = None
    size: Optional[str] = None
    weight: Optional[float] = None
    sku: str

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "quantity": self.quantity,
            "category": self.category,
            "brand": self.brand,
            "color": self.color,
            "size": self.size,
            "weight": self.weight,
            "sku": self.sku
        }