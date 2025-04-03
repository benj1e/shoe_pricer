from fastapi.testclient import TestClient

def test_create_shoe(client: TestClient, setup_db):
    """Test creating a new shoe."""
    store_response = client.post("/stores/", json={"name": "Adidas Store", "url": "https://adidas.com"})
    store_id = store_response.json()["id"]

    shoe_data = {"name": "Adidas UltraBoost", "brand": "Adidas", "price": 200, "store_id": store_id}
    response = client.post("/shoes/", json=shoe_data)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Adidas UltraBoost"

def test_get_shoes(client: TestClient, setup_db):
    """Test retrieving shoes."""
    response = client.get("/shoes/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
