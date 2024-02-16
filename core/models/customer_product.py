from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Text, ForeignKey, relationship

if TYPE_CHECKING:
    from .product import Product  # noqa: F401


class CustomerProduct(Base):
    __tablename__ = "customer_products"

    name: Mapped[str] = mapped_column(
        Text,
        default="",
        server_default="",
    )

    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id"),
        nullable=False,
    )

    product: Mapped["Product"] = mapped_column(
        relationship("Product", back_populates="customer_products"),
    )

    def __repr__(self):
        return f"<CustomerProduct(name={self.name})>"
