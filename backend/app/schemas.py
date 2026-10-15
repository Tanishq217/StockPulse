from datetime import datetime
from typing import Optional, Dict
from pydantic import BaseModel, Field, ConfigDict

class InventoryItemBase(BaseModel):
    sku: str = Field(..., min_length=2, max_length=50, examples=["SKU-ELEC-1001"])
    name: str = Field(..., min_length=2, max_length=150, examples=["Industrial Sensor Node"])
    category: str = Field(..., min_length=2, max_length=100, examples=["Electronics"])
    quantity: int = Field(default=0, ge=0, examples=[50])
    min_threshold: int = Field(default=10, ge=0, examples=[10])
    unit_price: float = Field(default=0.0, ge=0.0, examples=[49.99])
    supplier: Optional[str] = Field(None, max_length=150, examples=["Apex Components Inc."])
    location: Optional[str] = Field(None, max_length=100, examples=["Warehouse 2 - Shelf B3"])

class InventoryItemCreate(InventoryItemBase):
    pass

class InventoryItemUpdate(BaseModel):
    sku: Optional[str] = Field(None, min_length=2, max_length=50)
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    category: Optional[str] = Field(None, min_length=2, max_length=100)
    quantity: Optional[int] = Field(None, ge=0)
    min_threshold: Optional[int] = Field(None, ge=0)
    unit_price: Optional[float] = Field(None, ge=0.0)
    supplier: Optional[str] = Field(None, max_length=150)
    location: Optional[str] = Field(None, max_length=100)

class InventoryItemResponse(InventoryItemBase):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class InventoryStatsResponse(BaseModel):
    total_skus: int
    total_units: int
    total_valuation: float
    low_stock_count: int
    out_of_stock_count: int
    in_stock_count: int
    categories: Dict[str, int]

class HealthStatus(BaseModel):
    status: str
    version: str
    app: str

class ReadinessStatus(BaseModel):
    status: str
    database: str
