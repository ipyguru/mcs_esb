from typing import TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String

if TYPE_CHECKING:
    from .customer_product import CustomerProduct  # noqa: F401


class Product(Base):
    __tablename__ = "products"

    name: Mapped[str] = mapped_column(String(150))

    customer_products: Mapped[list["CustomerProduct"]] = relationship(
        back_populates="product"
    )

    def __repr__(self):
        return f"<Product(name={self.name})>"
