from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List
from .schemas import User as UserSchema, Product as ProductSchema, UserProducts
from .models import User, Product, UserProduct
from .database import get_db

router = APIRouter()

@router.post("/users", response_model=UserSchema)
async def create_user(user: UserSchema, db: AsyncSession = Depends(get_db)):
    # Check if user with the same ID or email already exists
    result = await db.execute(select(User).filter((User.id == user.id) | (User.email == user.email)))
    existing_user = result.scalars().first()
    if existing_user:
        if existing_user.id == user.id:
            raise HTTPException(status_code=400, detail="User ID already exists.")
        if existing_user.email == user.email:
            raise HTTPException(status_code=400, detail="Email already registered.")
    
    new_user = User(id=user.id, name=user.name, email=user.email)
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user

@router.get("/users", response_model=List[UserSchema])
async def get_users(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users

@router.get("/products", response_model=List[ProductSchema])
async def get_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    products = result.scalars().all()
    return products

@router.post("/users/{user_id}/products", response_model=List[ProductSchema])
async def add_user_products(user_id: int, user_products_data: UserProducts, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    product_list = []
    for product_id in user_products_data.product_ids:
        result = await db.execute(select(Product).filter(Product.id == product_id))
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")

        # Create an association entry
        user_product = UserProduct(user_id=user_id, product_id=product_id)
        db.add(user_product)
        product_list.append(product)

    await db.commit()
    return product_list

@router.get("/users/{user_id}/products", response_model=List[ProductSchema])
async def get_user_products(user_id: int, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Fetch products associated with the user
    result = await db.execute(
        select(Product).join(UserProduct).filter(UserProduct.user_id == user_id)
    )
    products = result.scalars().all()
    return products

@router.post("/users/{user_id}/purchase", response_model=List[ProductSchema])
async def purchase_product(user_id: int, purchase_data: UserProducts, db: AsyncSession = Depends(get_db)):
    # Check if user exists
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    purchased_products = []
    for product_id in purchase_data.product_ids:
        result = await db.execute(select(Product).filter(Product.id == product_id))
        product = result.scalars().first()
        if not product:
            raise HTTPException(status_code=404, detail=f"Product with id {product_id} not found")
        
        # Check if the product is already associated with the user
        result = await db.execute(
            select(UserProduct).filter(UserProduct.user_id == user_id, UserProduct.product_id == product_id)
        )
        existing_purchase = result.scalars().first()
        if existing_purchase:
            continue

        # Create a new association entry
        user_product = UserProduct(user_id=user_id, product_id=product_id)
        db.add(user_product)
        purchased_products.append(product)

    await db.commit()
    return purchased_products
