import pika

from typing import List

from fastapi import APIRouter, status, HTTPException, Depends

from sqlalchemy.ext.asyncio import AsyncSession

from . import crud
from .schemas import (
    Product,
    ProductCreate,
    ProductUpdate,
    ProductUpdatePartial,
    ProductPublic,
)
from .dependencies import get_product_by_id
from core.models import helper
from .utils import publish_to_rabbitmq

router = APIRouter(tags=["Products"])

# подключение к RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.queue_declare(queue="products", durable=True)
channel.queue_declare(queue="products.unf", durable=True)
channel.queue_declare(queue="products.bp16", durable=True)


@router.get("/", response_model=List[Product])
async def get_products(session: AsyncSession = Depends(helper.dependency)):
    return await crud.get_products(session=session)


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create_product(
    product: ProductCreate, session: AsyncSession = Depends(helper.dependency)
):
    try:
        created_product: Product = await crud.create_product(
            session=session, product=product
        )
    except Exception as e:
        error = f"Ошибка создания товара:\n {e}"
        if "UNIQUE constraint failed: products.guid_pr" in str(e):
            error = f"Товар с таким guid_pr ({product.guid_pr}) уже существует"
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
        ) from e

    # Получим представление товара для отправки в очередь
    public_product = ProductPublic.from_orm(created_product)  # noqa

    # Выбор маршрута
    routing_key = "products.unf" if created_product.guid_bp else "products.bp16"

    # Отправка в очередь
    await publish_to_rabbitmq(
        channel=channel, public_product=public_product, routing_key=routing_key
    )

    return created_product


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
