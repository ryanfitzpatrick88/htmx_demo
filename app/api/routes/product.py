from asyncio import sleep
from typing import Dict, List

from fastapi import Request, Body, HTTPException, FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import APIRouter
from pydantic import ValidationError

from app.core.event_bus import ConnectionManager
from app.crud.product import CRUDProduct
from app.api.dependencies.product_db import JSONProductDatabase
from app.models.product import Product, Category
from app.schemas.product import ProductCreate, ProductUpdateModel
from fastapi import APIRouter, Form
from fastapi.responses import RedirectResponse, JSONResponse
from app.api.dependencies.auth import validate_user_token
from fastapi import Depends
from enum import Enum
import json


from app.services.product_service import ProductService

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()
event_bus = ConnectionManager()

@router.get("/edit/{id}", response_class=HTMLResponse)
async def read_product(request: Request, id: int, user=Depends(validate_user_token)):
    product = CRUDProduct.get_product_by_id(id)
    return templates.TemplateResponse("product_detail.html", {"request": request, "product": product, "user": user})

@router.get("/", response_class=HTMLResponse)
async def list_products_page(request: Request, user=Depends(validate_user_token)):
    products = CRUDProduct.get_all_products()
    category_options = [category.value for category in Category]
    return templates.TemplateResponse("product_list.html", {"request": request,
                                                            "products": products,
                                                            "user": user,
                                                            "category_options": category_options})

@router.post("/add")
async def add_product(name: str = Form(...),
                        description: str = Form(...),
                        price: float = Form(...),
                        quantity: int = Form(...),
                        category: str = Form(...),
                        brand: str = Form(...),
                        color: str = Form(...),
                        size: str = Form(...),
                        weight: float = Form(...),
                        sku: str = Form(...),
                        user=Depends(validate_user_token)):
    id = len(CRUDProduct.get_all_products()) + 1
    product = Product(id=id, name=name, description=description, price=price, quantity=quantity, category=category, brand=brand, color=color, size=size, weight=weight, sku=sku)
    new_product = CRUDProduct.create_product(product)

    product_payload = new_product.json()

    await event_bus.broadcast(product_payload)

    response = HTMLResponse(content="Product added successfully")
    return response

@router.patch("/update/{product_id}", response_model=ProductUpdateModel)
async def update_product(product_id: int,
                         updates: Dict[str, str] = Body(..., embed=False)):
    db_product = CRUDProduct.get_product_by_id(product_id)
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Update the product with the provided values
    try:
        updated_data = {**db_product, **updates}  # Merge the existing data with updates
        updated_product = Product(**updated_data)  # Create a new Pydantic model instance with the updated data
    except ValidationError as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Update the product in the database
    db_product = CRUDProduct.update_product(product_id, updated_product)

    product_payload = json.dumps(db_product)

    await event_bus.broadcast(product_payload)

    # Return the updated product attributes (or adjust according to your needs)
    return {"updates": updates, "product": updated_product}

@router.get("/search", response_class=HTMLResponse)
async def search_products(request: Request,  query: str = "", user=Depends(validate_user_token)):
    # Assume `search_products()` retrieves your product data
    products = CRUDProduct.get_all_products()
    # sleep(5)  # Simulate a slow API
    await sleep(1)
    return templates.TemplateResponse("partials/product_search.html",
                                      {"request": request, "products": products, "user": user})

@router.get("/categories", response_class=HTMLResponse)
def read_root(request: Request):

    return templates.TemplateResponse("index.html", {"request": request, "fruit_options": category_options})
