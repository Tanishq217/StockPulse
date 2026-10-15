import logging
from typing import List, Optional
from fastapi import FastAPI, Depends, HTTPException, Query, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.orm import Session
from prometheus_fastapi_instrumentator import Instrumentator

from app.config import settings
from app.db import get_db, Base, engine
from app.models import InventoryItem
from app.schemas import (
    InventoryItemCreate,
    InventoryItemUpdate,
    InventoryItemResponse,
    InventoryStatsResponse,
    HealthStatus,
    ReadinessStatus,
)

from contextlib import asynccontextmanager

logger = logging.getLogger("stockpulse")
logging.basicConfig(level=logging.INFO)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database tables on application startup
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables initialized successfully")
    except Exception as exc:
        logger.warning(f"Database table initialization deferred: {exc}")
    yield

app = FastAPI(
    title="StockPulse API",
    description="Enterprise Warehouse & Inventory Management REST API",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expose Prometheus metrics on /metrics
instrumentator = Instrumentator()
instrumentator.instrument(app).expose(app, endpoint="/metrics")

@app.get("/", tags=["System"])
def root():
    return {
        "app": settings.app_name,
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health",
        "ready": "/ready",
        "metrics": "/metrics",
    }

@app.get("/health", response_model=HealthStatus, tags=["System"])
def health():
    """Liveness probe: verifies that the FastAPI process is responsive."""
    return HealthStatus(
        status="up",
        version="1.0.0",
        app=settings.app_name,
    )

@app.get("/ready", response_model=ReadinessStatus, tags=["System"])
def ready(db: Session = Depends(get_db)):
    """Readiness probe: verifies database connectivity before accepting traffic."""
    try:
        db.execute(text("SELECT 1"))
        return ReadinessStatus(status="ready", database="connected")
    except Exception as exc:
        logger.error(f"Readiness check failed: {exc}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Database connectivity unavailable",
        )

@app.get("/api/inventory/stats", response_model=InventoryStatsResponse, tags=["Inventory"])
def get_inventory_stats(db: Session = Depends(get_db)):
    """Calculates live KPI metrics and aggregate stock valuations."""
    items = db.query(InventoryItem).all()
    total_skus = len(items)
    total_units = sum(item.quantity for item in items)
    total_valuation = round(sum(item.quantity * item.unit_price for item in items), 2)
    low_stock_count = sum(1 for item in items if 0 < item.quantity <= item.min_threshold)
    out_of_stock_count = sum(1 for item in items if item.quantity == 0)
    in_stock_count = sum(1 for item in items if item.quantity > item.min_threshold)

    categories = {}
    for item in items:
        categories[item.category] = categories.get(item.category, 0) + 1

    return InventoryStatsResponse(
        total_skus=total_skus,
        total_units=total_units,
        total_valuation=total_valuation,
        low_stock_count=low_stock_count,
        out_of_stock_count=out_of_stock_count,
        in_stock_count=in_stock_count,
        categories=categories,
    )

@app.get("/api/inventory", response_model=List[InventoryItemResponse], tags=["Inventory"])
def list_inventory(
    q: Optional[str] = Query(None, description="Search by name or SKU"),
    category: Optional[str] = Query(None, description="Filter by category"),
    stock_status: Optional[str] = Query(None, description="Filter by status: in_stock, low_stock, out_of_stock"),
    db: Session = Depends(get_db),
):
    """Retrieve all inventory items with optional search and category filters."""
    query = db.query(InventoryItem)

    if q:
        query = query.filter(
            (InventoryItem.name.ilike(f"%{q}%")) | (InventoryItem.sku.ilike(f"%{q}%"))
        )
    if category:
        query = query.filter(InventoryItem.category == category)

    items = query.order_by(InventoryItem.updated_at.desc()).all()

    if stock_status:
        items = [item for item in items if item.status == stock_status]

    return items

@app.post("/api/inventory", response_model=InventoryItemResponse, status_code=status.HTTP_201_CREATED, tags=["Inventory"])
def create_inventory_item(item_in: InventoryItemCreate, db: Session = Depends(get_db)):
    """Register a new item in the warehouse inventory catalog."""
    existing = db.query(InventoryItem).filter(InventoryItem.sku == item_in.sku).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"An item with SKU '{item_in.sku}' already exists",
        )

    item = InventoryItem(**item_in.model_dump())
    db.add(item)
    db.commit()
    db.refresh(item)
    logger.info(f"Created inventory item id={item.id} sku={item.sku}")
    return item

@app.get("/api/inventory/{item_id}", response_model=InventoryItemResponse, tags=["Inventory"])
def get_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """Fetch complete details for a single inventory item by ID."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with id {item_id} not found",
        )
    return item

@app.put("/api/inventory/{item_id}", response_model=InventoryItemResponse, tags=["Inventory"])
def update_inventory_item(
    item_id: int, item_update: InventoryItemUpdate, db: Session = Depends(get_db)
):
    """Update stock quantity, threshold, pricing, or metadata for an existing item."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with id {item_id} not found",
        )

    update_data = item_update.model_dump(exclude_unset=True)

    if "sku" in update_data and update_data["sku"] != item.sku:
        existing_sku = (
            db.query(InventoryItem)
            .filter(InventoryItem.sku == update_data["sku"], InventoryItem.id != item_id)
            .first()
        )
        if existing_sku:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"SKU '{update_data['sku']}' is already assigned to another item",
            )

    for field, val in update_data.items():
        setattr(item, field, val)

    db.commit()
    db.refresh(item)
    logger.info(f"Updated inventory item id={item.id}")
    return item

@app.delete("/api/inventory/{item_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["Inventory"])
def delete_inventory_item(item_id: int, db: Session = Depends(get_db)):
    """Remove an item from the warehouse catalog."""
    item = db.query(InventoryItem).filter(InventoryItem.id == item_id).first()
    if not item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Inventory item with id {item_id} not found",
        )
    db.delete(item)
    db.commit()
    logger.info(f"Deleted inventory item id={item_id}")
    return None
