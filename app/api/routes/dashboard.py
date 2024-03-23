from fastapi.templating import Jinja2Templates
from app.api.dependencies.auth import validate_user_token
from fastapi import APIRouter, Request, Depends


router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.get("/")
async def read_dashboard(request: Request, user=Depends(validate_user_token)):
     # Dashboard data loading logic here
    data = {"request": request, "user": user}
    return templates.TemplateResponse("dashboard.html", data)
