from typing import List

from fastapi import APIRouter, status, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Product, ProductCreate
from core.models import helper


router = APIRouter(tags=["Products"])


@router.get("/", response_model=List[Product])
async def get_products(session: AsyncSession = Depends(helper.dependency)):
    return await crud.get_products(session=session)


@router.post("/", response_model=Product)
async def create_product(
    product: ProductCreate, session: AsyncSession = Depends(helper.dependency)
):
    return await crud.create_product(session=session, product=product)


@router.get("/{product_id}/", response_model=Product)
async def get_product(
    product_id: int,
    session: AsyncSession = Depends(helper.dependency),
):
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{product_id}'- is not found",
        )
    return product
