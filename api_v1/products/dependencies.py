from typing import Annotated

from fastapi import Path, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import helper, Product
from . import crud


async def get_product_by_id(
    product_id: Annotated[int, Path],
    session: AsyncSession = Depends(helper.dependency),
) -> Product:
    product = await crud.get_product_by_id(session=session, product_id=product_id)
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product '{product_id}'- is not found",
        )
    return product
