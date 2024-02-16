from .base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String


class CustomerProduct(Base):
    __tablename__ = "customer_products"

    name: Mapped[str] = mapped_column(String(150))

    def __repr__(self):
        return f"<CustomerProduct(name={self.name})>"
