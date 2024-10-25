from pydantic import BaseModel, EmailStr
from typing import List

class User(BaseModel):
    id: int
    name: str
    email: EmailStr

class Product(BaseModel):
    id: int
    name: str
    price: float

class UserProducts(BaseModel):
    product_ids: List[int]