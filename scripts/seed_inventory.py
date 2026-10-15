#!/usr/bin/env python3
"""Seed script to populate StockPulse with realistic warehouse inventory items."""
import os
import sys

# Add parent directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "backend"))

from app.db import SessionLocal
from app.models import InventoryItem

SAMPLE_ITEMS = [
    {
        "sku": "SKU-ELEC-1001",
        "name": "Industrial Edge IoT Gateway",
        "category": "Electronics",
        "quantity": 38,
        "min_threshold": 10,
        "unit_price": 189.50,
        "supplier": "Siemens Digital Industries",
        "location": "Warehouse 1 - Rack A1",
    },
    {
        "sku": "SKU-ELEC-1002",
        "name": "Arm Cortex-M4 Microcontroller Kit",
        "category": "Electronics",
        "quantity": 8,
        "min_threshold": 15,
        "unit_price": 34.90,
        "supplier": "STMicroelectronics",
        "location": "Warehouse 1 - Rack A2",
    },
    {
        "sku": "SKU-ROBO-2001",
        "name": "NEMA 23 High-Torque Stepper Motor",
        "category": "Robotics",
        "quantity": 64,
        "min_threshold": 20,
        "unit_price": 42.00,
        "supplier": "Oriental Motor Co.",
        "location": "Warehouse 1 - Rack B1",
    },
    {
        "sku": "SKU-ROBO-2002",
        "name": "Optical Rotary Encoder 1000PPR",
        "category": "Robotics",
        "quantity": 3,
        "min_threshold": 10,
        "unit_price": 68.75,
        "supplier": "Omron Automation",
        "location": "Warehouse 1 - Rack B2",
    },
    {
        "sku": "SKU-ELEC-3001",
        "name": "Solid State Relay 40A 240VAC",
        "category": "Electrical",
        "quantity": 112,
        "min_threshold": 25,
        "unit_price": 14.50,
        "supplier": "Crydom Inc.",
        "location": "Warehouse 2 - Bay C1",
    },
    {
        "sku": "SKU-ELEC-3002",
        "name": "DIN-Rail Switching Power Supply 24V 10A",
        "category": "Electrical",
        "quantity": 0,
        "min_threshold": 12,
        "unit_price": 58.00,
        "supplier": "Mean Well Enterprises",
        "location": "Warehouse 2 - Bay C2",
    },
    {
        "sku": "SKU-HARD-4001",
        "name": "M8 Stainless Steel Hex Flange Bolt (100pk)",
        "category": "Hardware",
        "quantity": 350,
        "min_threshold": 50,
        "unit_price": 12.20,
        "supplier": "Fastenal Industrial",
        "location": "Warehouse 3 - Bin H1",
    },
    {
        "sku": "SKU-TOOL-5001",
        "name": "Digital Caliper 150mm Stainless",
        "category": "Tools",
        "quantity": 18,
        "min_threshold": 5,
        "unit_price": 45.00,
        "supplier": "Mitutoyo Corporation",
        "location": "Tool Crib - Shelf 4",
    },
]

def seed():
    db = SessionLocal()
    try:
        created_count = 0
        for item_data in SAMPLE_ITEMS:
            existing = db.query(InventoryItem).filter(InventoryItem.sku == item_data["sku"]).first()
            if not existing:
                item = InventoryItem(**item_data)
                db.add(item)
                created_count += 1
        db.commit()
        print(f"Successfully seeded {created_count} inventory catalog items into database!")
    finally:
        db.close()

if __name__ == "__main__":
    seed()
