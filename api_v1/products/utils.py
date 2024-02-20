import asyncio
import json
from enum import Enum

import pika

from api_v1.products.schemas import ProductPublic


# class EnumEncoder(json.JSONEncoder):
#     def default(self, obj):
#         if isinstance(obj, Enum):
#             return obj.value
#         return super().default(obj)


async def publish_to_rabbitmq(channel, public_product: ProductPublic, routing_key: str):
    await asyncio.get_event_loop().run_in_executor(
        None,
        lambda: channel.basic_publish(
            exchange="",
            routing_key=routing_key,
            # body=json.dumps(public_product.dict(), ensure_ascii=False, cls=EnumEncoder),
            body=public_product.model_dump_json(),
            properties=pika.BasicProperties(
                delivery_mode=pika.DeliveryMode.Persistent,
            ),
        ),
    )
