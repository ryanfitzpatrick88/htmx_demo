from typing import Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.templating import Jinja2Templates
from jose import JWTError, jwt
from app.crud.user import CRUDUser
from app.core.config import settings
from app.schemas.token import TokenData
from fastapi import Cookie
from app.models.user import User
from fastapi.requests import Request
from app.core.unauthorized_exception import UnauthenticatedAccessException


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
templates = Jinja2Templates(directory="app/templates")

async def get_current_user(token: str = Depends(oauth2_scheme)) -> Optional[str]:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = CRUDUser.get_user_by_username(token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def validate_user_token(request: Request, access_token: str = Cookie(None)):
    result = await get_user_for_token(access_token)
    if not result:
        raise UnauthenticatedAccessException

    return result

async def get_user_for_token(access_token: str = Cookie(None)) -> User | None:
    # decode token and get user
    if not access_token:
        return None
    try:
        payload = jwt.decode(access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        token_data = TokenData(username=username)
    except JWTError:
        return None
    user = CRUDUser.get_user_by_username(token_data.username)
    if user is None:
        return None
    return user
