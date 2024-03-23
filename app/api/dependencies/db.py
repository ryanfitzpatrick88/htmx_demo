import json
from typing import Optional

from app.models import User


class JSONDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def read_db(self):
        try:
            with open(self.db_path, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def write_db(self, data):
        with open(self.db_path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_user_by_username(self, username: str) -> Optional[dict]:
        users = self.read_db()
        for user in users:
            if user['username'] == username:
                return user
        return None

    def create_user(self, user: User) -> dict:
        users = self.read_db()
        user_dict = user.to_dict()
        users.append(user_dict)
        self.write_db(users)
        return user

    def update_user(self, username: str, new_user_data: dict) -> Optional[dict]:
        users = self.read_db()
        for index, user in enumerate(users):
            if user['username'] == username:
                users[index].update(new_user_data)
                self.write_db(users)
                return users[index]
        return None

    def delete_user(self, username: str) -> bool:
        users = self.read_db()
        initial_length = len(users)
        users = [user for user in users if user['username'] != username]
        self.write_db(users)
        return len(users) < initial_length
