from typing import List

from fastapi import APIRouter, status, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial
from .dependencies import get_product_by_id
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
async def get_product(product: Product = Depends(get_product_by_id)):
    return product


@router.put("/{product_id}/")
async def update_product(
    product_update: ProductUpdate,
    product: Product = Depends(get_product_by_id),
    session: AsyncSession = Depends(helper.dependency),
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update
    )


@router.patch("/{product_id}/")
async def update_product_partial(
    product_update: ProductUpdatePartial,
    product: Product = Depends(get_product_by_id),
    session: AsyncSession = Depends(helper.dependency),
):
    return await crud.update_product(
        session=session, product=product, product_update=product_update, partial=True
    )
