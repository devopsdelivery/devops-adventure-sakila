from fastapi import APIRouter, HTTPException
from .schemas import User, Product, UserProducts
from .models import users, products, user_products
from typing import List

router = APIRouter()

@router.post("/users", response_model=User)
def create_user(user: User):
    users.append(user)
    user_products[user.id] = []
    return user

@router.get("/users", response_model=List[User])
def get_users():
    return users

@router.get("/products", response_model=List[Product])
def get_products():
    return products

@router.post("/users/{user_id}/products", response_model=List[Product])
def add_user_products(user_id: int, user_products_data: UserProducts):
    if user_id not in [user.id for user in users]:
        raise HTTPException(status_code=404, detail="User not found")

    product_list = []
    for product_id in user_products_data.product_ids:
        product = next((prod for prod in products if prod["id"] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
        product_list.append(product)

    user_products[user_id].extend(product_list)
    return user_products[user_id]

@router.get("/users/{user_id}/products", response_model=List[Product])
def get_user_products(user_id: int):
    if user_id not in user_products:
        raise HTTPException(status_code=404, detail="User not found")
    return user_products[user_id]
