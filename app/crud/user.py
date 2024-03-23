# Assuming pwd_context is from PassLib, if not, adjust accordingly
from passlib.context import CryptContext

from app.schemas.user import UserCreate

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

from app.models.user import User
from app.api.dependencies.db import JSONDatabase


db = JSONDatabase('db.json')

class CRUDUser:
    @staticmethod
    def get_user_by_username(username: str) -> User:
        return db.get_user_by_username(username)

    @staticmethod
    def create_user(user: UserCreate):
        user = User(username=user.username, email=user.email, hashed_password=pwd_context.hash(user.password))
        user.id = db.read_db()[-1]['id'] + 1 if db.read_db() else 1
        return db.create_user(user)

    @staticmethod
    def update_user(username: str, user: User) -> User:
        return db.update_user(username, user)

    @staticmethod
    def delete_user(username: str) -> None:
        db.delete_user(username)
