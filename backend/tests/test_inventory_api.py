from fastapi import status

def test_health_check(client):
    """Test the /health liveness probe."""
    response = client.get("/health")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "up"
    assert "version" in data
    assert "app" in data

def test_readiness_check(client):
    """Test the /ready readiness probe against the database."""
    response = client.get("/ready")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["status"] == "ready"
    assert data["database"] == "connected"

def test_metrics_endpoint(client):
    """Test the Prometheus /metrics endpoint."""
    response = client.get("/metrics")
    assert response.status_code == status.HTTP_200_OK
    assert "http_requests" in response.text or "process_virtual_memory_bytes" in response.text

def test_create_inventory_item(client):
    """Test creating a new inventory item with valid payload."""
    payload = {
        "sku": "SKU-TEST-001",
        "name": "Heavy Duty Industrial Relay",
        "category": "Electrical",
        "quantity": 45,
        "min_threshold": 10,
        "unit_price": 28.50,
        "supplier": "Omron Global",
        "location": "Warehouse A - Rack 3",
    }
    response = client.post("/api/inventory", json=payload)
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["id"] is not None
    assert data["sku"] == "SKU-TEST-001"
    assert data["name"] == "Heavy Duty Industrial Relay"
    assert data["status"] == "in_stock"
    assert data["quantity"] == 45

def test_create_duplicate_sku_fails(client):
    """Test that creating an item with an existing SKU returns HTTP 400."""
    payload = {
        "sku": "SKU-DUP-100",
        "name": "Thermal Sensor",
        "category": "Sensors",
        "quantity": 10,
        "min_threshold": 5,
        "unit_price": 12.00,
    }
    first_resp = client.post("/api/inventory", json=payload)
    assert first_resp.status_code == status.HTTP_201_CREATED

    second_resp = client.post("/api/inventory", json=payload)
    assert second_resp.status_code == status.HTTP_400_BAD_REQUEST
    assert "already exists" in second_resp.json()["detail"]

def test_get_inventory_item_by_id(client):
    """Test retrieving an item by its primary key ID."""
    payload = {
        "sku": "SKU-RET-200",
        "name": "Microcontroller Board v2",
        "category": "Electronics",
        "quantity": 8,
        "min_threshold": 15,
        "unit_price": 35.00,
    }
    create_resp = client.post("/api/inventory", json=payload)
    item_id = create_resp.json()["id"]

    get_resp = client.get(f"/api/inventory/{item_id}")
    assert get_resp.status_code == status.HTTP_200_OK
    data = get_resp.json()
    assert data["id"] == item_id
    assert data["sku"] == "SKU-RET-200"
    # Quantity (8) <= min_threshold (15) -> status should be 'low_stock'
    assert data["status"] == "low_stock"

def test_get_nonexistent_item_returns_404(client):
    """Test retrieving a missing item returns HTTP 404."""
    response = client.get("/api/inventory/999999")
    assert response.status_code == status.HTTP_404_NOT_FOUND

def test_list_inventory_and_filtering(client):
    """Test listing inventory with search query and category filters."""
    items = [
        {"sku": "SKU-A-1", "name": "Alloy Bolt 10mm", "category": "Hardware", "quantity": 100, "unit_price": 0.50},
        {"sku": "SKU-A-2", "name": "Alloy Nut 10mm", "category": "Hardware", "quantity": 120, "unit_price": 0.40},
        {"sku": "SKU-B-1", "name": "Step Motor Driver", "category": "Robotics", "quantity": 0, "unit_price": 45.00},
    ]
    for it in items:
        client.post("/api/inventory", json=it)

    # List all
    all_resp = client.get("/api/inventory")
    assert all_resp.status_code == status.HTTP_200_OK
    assert len(all_resp.json()) == 3

    # Filter by category
    cat_resp = client.get("/api/inventory?category=Hardware")
    assert len(cat_resp.json()) == 2

    # Filter by search query
    query_resp = client.get("/api/inventory?q=Motor")
    assert len(query_resp.json()) == 1
    assert query_resp.json()[0]["sku"] == "SKU-B-1"

    # Filter by status: out_of_stock
    oos_resp = client.get("/api/inventory?stock_status=out_of_stock")
    assert len(oos_resp.json()) == 1
    assert oos_resp.json()[0]["sku"] == "SKU-B-1"

def test_update_inventory_item(client):
    """Test updating fields of an existing inventory item."""
    create_resp = client.post("/api/inventory", json={
        "sku": "SKU-UPD-01",
        "name": "Stepper Motor",
        "category": "Robotics",
        "quantity": 5,
        "min_threshold": 10,
        "unit_price": 50.00,
    })
    item_id = create_resp.json()["id"]

    update_payload = {
        "quantity": 25,
        "unit_price": 48.00,
    }
    put_resp = client.put(f"/api/inventory/{item_id}", json=update_payload)
    assert put_resp.status_code == status.HTTP_200_OK
    data = put_resp.json()
    assert data["quantity"] == 25
    assert data["unit_price"] == 48.00
    # Now quantity 25 > min_threshold 10 -> in_stock
    assert data["status"] == "in_stock"

def test_delete_inventory_item(client):
    """Test deleting an inventory item."""
    create_resp = client.post("/api/inventory", json={
        "sku": "SKU-DEL-99",
        "name": "Disposable Calibrator",
        "category": "Tools",
        "quantity": 2,
        "min_threshold": 1,
        "unit_price": 15.00,
    })
    item_id = create_resp.json()["id"]

    del_resp = client.delete(f"/api/inventory/{item_id}")
    assert del_resp.status_code == status.HTTP_204_NO_CONTENT

    # Verify item is gone
    get_resp = client.get(f"/api/inventory/{item_id}")
    assert get_resp.status_code == status.HTTP_404_NOT_FOUND

def test_inventory_stats(client):
    """Test calculation of inventory stats and valuation."""
    client.post("/api/inventory", json={"sku": "ST-1", "name": "Item 1", "category": "CatA", "quantity": 10, "min_threshold": 5, "unit_price": 10.0})
    client.post("/api/inventory", json={"sku": "ST-2", "name": "Item 2", "category": "CatA", "quantity": 3, "min_threshold": 5, "unit_price": 20.0})
    client.post("/api/inventory", json={"sku": "ST-3", "name": "Item 3", "category": "CatB", "quantity": 0, "min_threshold": 5, "unit_price": 15.0})

    stats_resp = client.get("/api/inventory/stats")
    assert stats_resp.status_code == status.HTTP_200_OK
    stats = stats_resp.json()
    assert stats["total_skus"] == 3
    assert stats["total_units"] == 13
    # 10*10 + 3*20 + 0*15 = 100 + 60 = 160
    assert stats["total_valuation"] == 160.0
    assert stats["in_stock_count"] == 1
    assert stats["low_stock_count"] == 1
    assert stats["out_of_stock_count"] == 1
    assert stats["categories"]["CatA"] == 2
    assert stats["categories"]["CatB"] == 1
