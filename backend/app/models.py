from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Float, DateTime
from app.db import Base

class InventoryItem(Base):
    __tablename__ = "inventory_items"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String(50), unique=True, index=True, nullable=False)
    name = Column(String(150), index=True, nullable=False)
    category = Column(String(100), index=True, nullable=False)
    quantity = Column(Integer, default=0, nullable=False)
    min_threshold = Column(Integer, default=10, nullable=False)
    unit_price = Column(Float, default=0.0, nullable=False)
    supplier = Column(String(150), nullable=True)
    location = Column(String(100), nullable=True)
    created_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    @property
    def status(self) -> str:
        if self.quantity <= 0:
            return "out_of_stock"
        elif self.quantity <= self.min_threshold:
            return "low_stock"
        return "in_stock"
