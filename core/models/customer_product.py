from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Text, ForeignKey

from .base import Base

if TYPE_CHECKING:
    from .product import Product  # noqa: F401
    from .customer import Customer  # noqa: F401


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

    customer_id: Mapped[int] = mapped_column(
        ForeignKey("customers.id"),
        nullable=False,
    )

    product: Mapped["Product"] = relationship(
        "Product", back_populates="customer_products"
    )

    customer: Mapped["Customer"] = relationship(
        "Customer", back_populates="customer_products"
    )

    def __repr__(self):
        return f"<CustomerProduct(name={self.name})>"
