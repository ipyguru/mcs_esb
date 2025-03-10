import json
import pika
import logging
import time

from typing import List, Any
from pika.exceptions import AMQPConnectionError

from api_v1.esb.schemas import Package, GetMessages, PackageMessage, Ask, Exchange, Queue, Bind
from core.settings import settings

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class RabbitMQManager:
    def __init__(self):
        self.host = settings.rabbit.host
        self.params = pika.ConnectionParameters(self.host, heartbeat=580)
        self.connection = None
        self.channel = None

        self._connect()
        self.initialize_queues()

    def exchange_declare(self, exchange: Exchange):
        self.check_connection()

        # Создаем если не существует
        if exchange.exchange == "amq.topic":
            return

        self.channel.exchange_declare(
                exchange=exchange.exchange,
                exchange_type=exchange.exchange_type,
                durable=exchange.durable,
        )

    def queue_declare(self, queue: Queue):
        self.check_connection()
        self.channel.queue_declare(queue=queue.queue, durable=queue.durable)

    def queue_bind(self, bind: Bind):
        self.check_connection()

        self.channel.queue_bind(
            exchange=bind.exchange,
            queue=bind.queue,
            routing_key=bind.routing_key,
        )

    def initialize_queues(self):
        self.check_connection()

    def _connect(self):
        logger.info(f"Подключение к RabbitMQ: {self.host}")

        tries = 0
        while True:
            try:
                self.connection = pika.BlockingConnection(self.params)
                self.channel = self.connection.channel()
                if self.connection.is_open:
                    break
            except (AMQPConnectionError, Exception) as e:
                time.sleep(5)
                tries += 1
                if tries == 20:
                    raise AMQPConnectionError(e)

    def check_connection(self):
        if not self.connection or self.connection.is_closed:
            self._connect()

    def _get_message_body(self, queue):
        method_frame, _, body = self.channel.basic_get(queue, auto_ack=False)
        if method_frame:
            return json.loads(body), method_frame.delivery_tag
        return None, None

    def _count_messages(self, queue):
        cnt = self.channel.queue_declare(queue=queue, passive=True).method.message_count
        return cnt

    def publish_message(self, package: Package, message: List[Any]):
        self.check_connection()
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
            self.close()
            raise Exception(error)

    def get_messages(self, query: GetMessages):
        self.check_connection()

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
            self.close()
            raise Exception(error)

        return package_message

    def ask_messages(self, query: Ask):
        self.check_connection()

        cnt = len(query.delivery_tags)
        for tag in query.delivery_tags:
            try:
                self.channel.basic_ack(tag)
            except Exception as e:
                error = f"Ошибка подтверждения сообщения:\n {e}"
                return {"message": error}
        return {"message": f"{cnt} {self.plural_count(cnt)}- подтверждено"}

    def close(self):
        # Закрываем соединение
        if self.connection and self.connection.is_open:
            self.connection.close()

    @staticmethod
    def plural_count(count: int):
        if count % 10 == 1 and count % 100 != 11:
            return "сообщение"
        elif 2 <= count % 10 <= 4 and (count % 100 < 10 or count % 100 >= 20):
            return "сообщения"
        else:
            return "сообщений"
