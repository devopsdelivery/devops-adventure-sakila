from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str

class Product(BaseModel):
    id: int
    name: str
    price: float

class UserProducts(BaseModel):
    user_id: int
    product_ids: List[int]
