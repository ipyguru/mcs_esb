import json

import pika

from fastapi import APIRouter, status, HTTPException, Depends

from .schemas import Package
from core.settings import settings


router = APIRouter(tags=["Producer"])


@router.post("/", response_model=Package, status_code=status.HTTP_201_CREATED)
def post_messages(package: Package):
    """
    # Отправка сообщения в очередь
    ```1C

    ```
    """
    # подключение к RabbitMQ
    RabbitMQConnection = pika.BlockingConnection(
        pika.ConnectionParameters(settings.rabbit.host)
    )
    channel = RabbitMQConnection.channel()

    for message in package.package_messages.messages:
        try:
            channel.basic_publish(
                exchange=package.exchange,
                routing_key=package.routing_key,
                body=json.dumps(message),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )
        except Exception as e:
            error = f"Ошибка отправки сообщения в очередь:\n {e}"
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
            ) from e

    return package


#
#
# @router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
# async def create_product(
#     product: ProductCreate, session: AsyncSession = Depends(helper.dependency)
# ):
#     try:
#         created_product: Product = await crud.create_product(
#             session=session, product=product
#         )
#     except Exception as e:
#         error = f"Ошибка создания товара:\n {e}"
#         if "UNIQUE constraint failed: products.guid_pr" in str(e):
#             error = f"Товар с таким guid_pr ({product.guid_pr}) уже существует"
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST, detail=str(error)
#         ) from e
#
#     # Выбор маршрута
#     routing_key = "products.unf" if created_product.guid_bp else "products.bp16"
#
#     # Отправка в очередь
#     await publish_to_rabbitmq(
#         channel=channel,
#         public_product=ProductPublic.model_validate(created_product),
#         routing_key=routing_key,
#     )
#
#     return created_product
#
