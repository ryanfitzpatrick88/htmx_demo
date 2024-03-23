from pydantic import BaseModel
from typing import Optional, Dict

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    quantity: int
    category: str
    brand: str
    color: Optional[str] = None
    size: Optional[str] = None
    weight: Optional[float] = None
    sku: str

class ProductCreate(ProductBase):
    pass

class ProductUpdate(ProductBase):
    id: int

class ProductInDB(ProductBase):
    id: int

class Product(ProductInDB):
    pass

class ProductUpdateModel(BaseModel):
    updates: Dict[str, Optional[str]]