from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Union

from core.models import Product
from .schemas import ProductCreate


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
