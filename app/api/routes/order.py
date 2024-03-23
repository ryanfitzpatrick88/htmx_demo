from datetime import timedelta, datetime
from random import random, randint, choice, uniform, randrange
from typing import Dict, List

from fastapi import APIRouter, Response, Request, Depends, Body, Form, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from app.services.order_service import OrderService
from app.models.order import Order, OrderItem, OrderStatus
from fastapi.templating import Jinja2Templates
from app.api.dependencies.auth import validate_user_token
from app.crud.order import CRUDOrder

router = APIRouter()
order_service = OrderService('db_orders.json')
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def list_order_page(request: Request, user=Depends(validate_user_token)):
    orders = order_service.get_all_orders()
    return templates.TemplateResponse("order_list.html", {"request": request, "orders": orders, "user": user})

@router.get("/orders_list", response_class=HTMLResponse)
async def list_orders(request: Request, user=Depends(validate_user_token)):
    orders = order_service.get_all_orders()
    return templates.TemplateResponse("partials/order_list_partial.html", {"request": request, "orders": orders, "user": user})


@router.post("/add")
def add_order(order_date: str = Form(...),
              customer_id: int = Form(...),
              customer_name: str = Form(...),
              order_total: float = Form(...)):
    order = Order(order_id=0,
                  order_date=order_date,
                  customer_id=customer_id,
                  customer_name=customer_name,
                  order_total=order_total,
                  order_items=[])
    CRUDOrder.create_order(order)
    return {"message": "Order added successfully"}

@router.get("/edit/{order_id}", response_class=HTMLResponse)
async def get_order(request: Request, order_id: int, user=Depends(validate_user_token)):
    order = order_service.get_order_by_id(order_id)
    return templates.TemplateResponse("order_detail.html", { "request" : request,  "order": order, "user": user})

@router.post("/orders")
def create_order(order: Order):
    return order_service.create_order(order)

@router.put("/orders/{order_id}")
def update_order(order_id: int, order: Order):
    return order_service.update_order(order_id, order)

@router.delete("/orders/{order_id}")
def delete_order(order_id: int):
    return order_service.delete_order(order_id)

@router.patch("/update-item/{order_id}")
async def update_order_item(order_id: int,
                            order_item_id: int = Form(...),
                            product_id: int = Form(...),
                            product_name: str = Form(...),
                            item_quantity: int = Form(...),
                            item_price: int = Form(...),
                            user=Depends(validate_user_token)
                            ):
    db_order_json = CRUDOrder.get_order_by_id(order_id)
    if not db_order_json:
        raise HTTPException(status_code=404, detail="Order not found")

    db_order = Order(**db_order_json)

    item_id = order_item_id
    if item_id == 0:
        # id unique to all order items
        item_id = len(db_order.order_items) + 1 | 1
        order_item = OrderItem(order_item_id=item_id,
                               item_name=product_name,
                               item_price=item_price,
                               item_quantity=item_quantity,
                               product_id=product_id,
                               product_name=product_name)
        CRUDOrder.create_order_item(order_id, order_item.to_dict())
    else:
        # Update existing order item
        for index, item in enumerate(db_order.order_items):
            if item.order_item_id == item_id:
                db_order.order_items[index].item_quantity = item_quantity
                db_order.order_items[index].item_price = item_price
                db_order.order_items[index].product_id = product_id
                db_order.order_items[index].product_name = product_name
                CRUDOrder.update_order(order_id, db_order.to_dict())
                break
        pass

@router.get("/order_plan_day", response_class=HTMLResponse)
def get_partial_content(request: Request, date: str, user=Depends(validate_user_token)):
    orders = CRUDOrder.get_orders_by_date(date)
    order_count = len(orders)
    order_total = sum([order['order_total'] for order in orders])
    return templates.TemplateResponse("partials/order_plan_day.html",
                                      { "request": request,
                                        "date": date,
                                        "orders": orders,
                                        "order_count": order_count,
                                        "order_total": order_total,
                                       })

@router.get("/order_segment_day", response_class=HTMLResponse)
def get_order_segment(request: Request, date: str, user=Depends(validate_user_token)):
    return templates.TemplateResponse("partials/order_segment_day.html", {"request": request, "date": date, "user": user})


@router.get("/order_plan", response_class=HTMLResponse)
def get_order_plan(request: Request, user=Depends(validate_user_token)):
    return templates.TemplateResponse("order_plan.html", {"request": request, "user": user})

# Sample data lists
customer_names = ["Alice", "Bob", "Charlie", "David", "Eve", "Fiona", "George", "Hannah", "Ivan", "Jane"]
item_names = ["ItemA", "ItemB", "ItemC", "ItemD", "ItemE", "ItemF", "ItemG", "ItemH", "ItemI", "ItemJ"]
product_names = ["ProductA", "ProductB", "ProductC", "ProductD", "ProductE", "ProductF", "ProductG", "ProductH", "ProductI", "ProductJ"]
statuses = list(OrderStatus)

def random_date(start, end):
    """Generate a random datetime between `start` and `end`."""
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)

@router.post("/generate")
def generate_orders(order_count: int = Form(...),
                    start_date: str = Form(...),
                    end_date: str = Form(...)):
    try:
        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format, use YYYY-MM-DD.")

    orders = []
    for _ in range(order_count):
        order_id = randint(1, 10)
        order_date = random_date(start, end).strftime("%Y-%m-%d")
        customer_id = randint(1, 10)
        customer_name = choice(customer_names)
        order_status = choice(statuses)
        order_items = []
        for _ in range(randint(1, 3)):  # Each order will have 1 to 3 items
            order_item = OrderItem(
                order_item_id=randint(1, 10),
                item_name=choice(item_names),
                item_price=uniform(10, 100),
                item_quantity=randint(1, 10),
                product_id=randint(1, 10),
                product_name=choice(product_names)
            )
            order_items.append(order_item)
        order = Order(
            order_id=order_id,
            order_date=order_date,
            customer_id=customer_id,
            customer_name=customer_name,
            order_status=order_status,
            order_items=order_items,
            order_total=0
        )
        order.calculate_order_total()  # Update order total based on items
        orders.append(order)

    for order in orders:
        CRUDOrder.create_order(order)

    return orders
