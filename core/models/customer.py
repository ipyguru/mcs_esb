from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Text

if TYPE_CHECKING:
    from .customer_product import CustomerProduct  # noqa: F401


class Customer(Base):
    __tablename__ = "customers"

    name: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    inn: Mapped[str] = mapped_column(String(12), unique=True)

    customer_products: Mapped[list["CustomerProduct"]] = relationship(
        back_populates="customer"
    )

    def __repr__(self):
        return f"<Customer(inn={self.inn}, name={self.name})>"
