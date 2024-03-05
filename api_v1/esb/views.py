from fastapi import APIRouter, status, HTTPException
from starlette.responses import JSONResponse

from . import RabbitMQManager
from .schemas import Package, PackageMessage, GetMessages, Ask


router = APIRouter(tags=["esb"])

rabbitmq_manager = RabbitMQManager()


@router.post("/publish", response_model=Package, status_code=status.HTTP_201_CREATED)
def publish_messages(package: Package):
    """
    # Отправка сообщения в очередь
    ```1C

    ```
    """
    for message in package.package_messages.messages:
        try:
            rabbitmq_manager.publish_message(package, message)
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail=str(e)
            ) from e

    return package


@router.post("/get", response_model=PackageMessage, status_code=status.HTTP_200_OK)
def get_messages(query: GetMessages):
    """
    # Получение сообщений из очереди
    """
    package_message = rabbitmq_manager.get_messages(query)
    return package_message


@router.post("/ask", status_code=status.HTTP_200_OK)
def ask_messages(query: Ask):
    """
    # Подтверждение получения сообщений из очереди
    """

    response = rabbitmq_manager.ask_messages(query)
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)
