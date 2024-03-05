import json
import pika

from typing import List, Any

from api_v1.esb.schemas import Package, GetMessages, PackageMessage, Ask
from core.settings import settings


class RabbitMQManager:
    def __init__(self):
        self.host = settings.rabbit.host
        self.params = pika.ConnectionParameters(self.host)
        self.connection = None
        self.channel = None

    def connect(self):
        if not self.connection or self.connection.is_closed:
            self.connection = pika.BlockingConnection(self.params)
            self.channel = self.connection.channel()

    def ensure_connection(self):
        if not self.connection or self.connection.is_closed:
            self.connect()
            # Нужно подождать, пока канал будет открыт
            while not self.connection.is_open:
                continue

    def __del__(self):
        if self.connection and self.connection.is_open:
            self.connection.close()

    def _get_message_body(self, queue):
        method_frame, _, body = self.channel.basic_get(queue, auto_ack=False)
        if method_frame:
            return json.loads(body), method_frame.delivery_tag
        return None, None

    def _count_messages(self, queue):
        cnt = self.channel.queue_declare(queue=queue, passive=True).method.message_count
        return cnt

    def publish_message(self, package: Package, message: List[Any]):
        self.ensure_connection()
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
        self.ensure_connection()

        package_message = PackageMessage(messages=[])
        try:
            cnt = self._count_messages(query.queue)
            if cnt:
                for _ in range(cnt):
                    message, delivery_tag = self._get_message_body(query.queue)
                    if message:
                        package_message.messages.append(
                            {"message": message, "delivery_tag": delivery_tag}
                        )
                    else:
                        break
        except Exception as e:
            error = f"Ошибка получения сообщения из очереди:\n {e}"
            raise Exception(error)
        return package_message

    def ask_messages(self, query: Ask):
        self.ensure_connection()

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
