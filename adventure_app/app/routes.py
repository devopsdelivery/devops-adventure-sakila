from fastapi import APIRouter, HTTPException
from .schemas import User, Product, UserProducts
from .models import users, products, user_products
from typing import List

router = APIRouter()

@router.post("/users", response_model=User)
def create_user(user: User):
    if any(existing_user.id == user.id for existing_user in users):
        raise HTTPException(status_code=400, detail="User ID already exists.")
    if any(existing_user.email == user.email for existing_user in users):
        raise HTTPException(status_code=400, detail="Email already registered.")
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

@router.post("/users/{user_id}/purchase", response_model=List[Product])
def purchase_product(user_id: int, purchase_data: UserProducts):
    # Check if user exists
    user = next((user for user in users if user.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    purchased_products = []
    for product_id in purchase_data.product_ids:
        product = next((prod for prod in products if prod["id"] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
        purchased_products.append(product)

    # Add the purchased products to the user's products
    user_products[user_id].extend(purchased_products)
    return user_products[user_id]
