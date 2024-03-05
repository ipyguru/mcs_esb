import json
from typing import List, Any

import pika

from api_v1.esb.schemas import Package, GetMessages, PackageMessage, Ask
from core.settings import settings


class RabbitMQManager:
    def __init__(self):
        self.host = settings.rabbit.host
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(self.host))
        self.channel = self.connection.channel()

    def __del__(self):
        self.connection.close()

    def publish_message(self, package: Package, message: List[Any]):
        try:
            self.channel.basic_publish(
                exchange=package.exchange,
                routing_key=package.routing_key,
                body=json.dumps(message, ensure_ascii=False),
                properties=pika.BasicProperties(
                    delivery_mode=2,  # make message persistent
                ),
            )
        except Exception as e:
            error = f"Ошибка отправки сообщения в очередь:\n {e}"
            raise Exception(error)

    def get_messages(self, query: GetMessages):
        package_message = PackageMessage(messages=[])
        cnt = self.channel.queue_declare(
            queue=query.queue, passive=True
        ).method.message_count
        if cnt:
            for count_massages in range(cnt):
                method_frame, header_frame, body = self.channel.basic_get(
                    query.queue, auto_ack=False
                )
                if method_frame:
                    body = {
                        "message": json.loads(body),
                        "delivery_tag": method_frame.delivery_tag,
                    }
                    package_message.messages.append(body)
                    # self.channel.basic_ack(method_frame.delivery_tag)
                else:
                    break
        return package_message

    def ask_messages(self, query: Ask):
        cnt = len(query.delivery_tags)
        for tag in query.delivery_tags:
            try:
                self.channel.basic_ack(tag)
            except Exception as e:
                error = f"Ошибка подтверждения сообщения:\n {e}"
                raise Exception(error)
        return {"message": f"{cnt} {self.plural_count(cnt)}- подтверждено"}

    @staticmethod
    def plural_count(count: int):
        if count % 10 == 1 and count % 100 != 11:
            return "сообщение"
        elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
            return "сообщения"
        else:
            return "сообщений"
