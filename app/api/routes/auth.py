from typing import Dict, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, Form, Request, Body
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from app.core.redirect_response import HTTPResponseHXRedirect
from app.crud.user import CRUDUser
from app.models import User
from app.schemas.user import UserCreate
from app.schemas.token import Token
from app.services.auth_service import create_access_token, authenticate_user
from app.api.dependencies.auth import oauth2_scheme, get_current_user, validate_user_token
from app.api.dependencies.forms import as_form

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/login")
async def login(request: Request, form_data: OAuth2PasswordRequestForm = Depends()):
    redirect_url = '/'
    response = HTTPResponseHXRedirect(redirect_url)
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )

    # response = JSONResponse(content={"message": "Login successful"})
    access_token = create_access_token(data={"sub": user.username})
    response.set_cookie(key="access_token", value=access_token, httponly=True)
    return response

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/logout")
async def logout(request: Request, user=Depends(validate_user_token)):
    redirect_url = '/auth/login'
    response = HTTPResponseHXRedirect(redirect_url)
    response.delete_cookie(key="access_token")
    return response

# ex: form_data: FormData = Depends(as_form(FormData))
@router.post("/register")
async def register(user_create: UserCreate):
    username = user_create.username
    db_user = CRUDUser.get_user_by_username(username)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered",
        )
    return CRUDUser.create_user(user_create)

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    return {
        "access_token": create_access_token(user.id),
    }