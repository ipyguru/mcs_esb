from __future__ import annotations

from typing import List, Any

from pydantic import BaseModel


class Package(BaseModel):
    exchange: str = "amq.topic"
    routing_key: str
    package_messages: PackageMessage
    queue: str = ""


class PackageMessage(BaseModel):
    messages: List[Any]
