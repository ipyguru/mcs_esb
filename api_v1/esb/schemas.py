from __future__ import annotations

from typing import List, Any

from pydantic import BaseModel


class Exchange(BaseModel):
    exchange: str = "amq.topic"
    exchange_type: str = "topic"
    durable: bool = True


class Queue(BaseModel):
    queue: str
    durable: bool = True


class Bind(BaseModel):
    exchange: str = "amq.topic"
    queue: str
    routing_key: str


class Package(BaseModel):
    exchange: str = "amq.topic"
    routing_key: str
    package_messages: PackageMessage
    queue: str = ""


class PackageMessage(BaseModel):
    messages: List[Any]


class GetMessages(BaseModel):
    exchange: str = "amq.topic"
    queue: str


class Ask(BaseModel):
    delivery_tags: List[int]
