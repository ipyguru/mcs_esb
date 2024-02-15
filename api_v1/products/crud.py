from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union, Any

from core.models import Product
from .schemas import ProductCreate, ProductUpdate, ProductUpdatePartial


async def get_products(session: AsyncSession) -> List[Product]:
    stmt = select(Product).order_by(Product.id)
    result: Result = await session.execute(stmt)
    return list(result.scalars().all())


async def get_product_by_id(
    session: AsyncSession, product_id: int
) -> Union[Product, None]:
    # stmt = select(Product).where(Product.id == product_id)
    # result: Result = await session.execute(stmt)
    # return result.scalar_one()
    return await session.get(Product, product_id)


async def create_product(session: AsyncSession, product: ProductCreate) -> Product:
    product = Product(**product.model_dump())
    session.add(product)
    await session.commit()
    await session.refresh(product)
    return product


async def update_product(
    session: AsyncSession,
    product: Product,
    product_update: Union[ProductUpdate, ProductUpdatePartial],
    partial: bool = False,
) -> Product:
    for key, value in product_update.model_dump(exclude_unset=partial).items():
        setattr(product, key, value)
    await session.commit()
    await session.refresh(product)
    return product
