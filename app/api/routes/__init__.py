from fastapi import APIRouter
from app.api.routes import auth, dashboard, product, order

router = APIRouter()
router.include_router(auth.router, tags=["auth"], prefix="/auth")
router.include_router(dashboard.router, tags=["dashboard"])
router.include_router(product.router, tags=["product"], prefix="/product")
router.include_router(order.router, tags=["order"], prefix="/order")
