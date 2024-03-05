import json

import pika

from fastapi import APIRouter, status, HTTPException

from .schemas import Package, Query, PackageMessage
from core.settings import settings


router = APIRouter(tags=["esb"])


@router.post("/publish", response_model=Package, status_code=status.HTTP_201_CREATED)
def publish_messages(package: Package):
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
                body=json.dumps(message, ensure_ascii=False),
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


@router.post("/get", response_model=PackageMessage, status_code=status.HTTP_200_OK)
def get_messages(query: Query):
    """
    # Получение сообщений из очереди
    """
    package_message = PackageMessage(messages=[])

    # подключение к RabbitMQ
    RabbitMQConnection = pika.BlockingConnection(
        pika.ConnectionParameters(settings.rabbit.host)
    )
    channel = RabbitMQConnection.channel()

    cnt = channel.queue_declare(queue=query.queue, passive=True).method.message_count
    if cnt:
        for count_massages in range(cnt):
            method_frame, header_frame, body = channel.basic_get(
                query.queue, auto_ack=False
            )
            if method_frame:
                body = {
                    "message": json.loads(body),
                    "delivery_tag": method_frame.delivery_tag,
                }
                package_message.messages.append(body)
                channel.basic_ack(method_frame.delivery_tag)
            else:
                break

    RabbitMQConnection.close()

    return package_message


# @router.post("/ask", status_code=status.HTTP_200_OK)
# def ask_messages(ask: Ask):
#     """
#     # Подтверждение получения сообщения из очереди
#     """
#
#     # подключение к RabbitMQ
#     RabbitMQConnection = pika.BlockingConnection(
#         pika.ConnectionParameters(settings.rabbit.host)
#     )
#     channel = RabbitMQConnection.channel()
#
#     channel.basic_ack(Ask.delivery_tag)
#     RabbitMQConnection.close()
#
#     return JSONResponse(
#         content={"message": f"Сообщение {Ask.delivery_tag} подтверждено"}
#     )
