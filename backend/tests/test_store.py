from fastapi.testclient import TestClient

def test_create_store(client: TestClient, setup_db):
    """Test creating a new store."""
    response = client.post("/stores/", json={"name": "Nike Store", "url": "https://nike.com"})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Nike Store"

def test_get_stores(client: TestClient, setup_db):
    """Test retrieving stores."""
    response = client.get("/stores/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_update_store(client: TestClient, setup_db):
    """Test updating a store."""
    response = client.post("/stores/", json={"name": "Old Store", "url": "https://oldstore.com"})
    store_id = response.json()["id"]

    update_data = {"name": "New Store"}
    update_response = client.patch(f"/stores/{store_id}", json=update_data)
    assert update_response.status_code == 200
    assert update_response.json()["name"] == "New Store"
