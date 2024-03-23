from fastapi import Form, Depends
from typing import Type, Callable
from pydantic import BaseModel

# Function to create a form parser dependency
def as_form(model: Type[BaseModel]) -> Callable:
    def _parse_form_data(**data):
        return model.parse_obj(data)
    return _parse_form_data