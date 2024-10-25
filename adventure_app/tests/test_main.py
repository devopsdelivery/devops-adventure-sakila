from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_user():
    response = client.post("/users", json={"id": 1, "name": "John Doe"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "John Doe"}

def test_get_users():
    client.post("/users", json={"id": 2, "name": "Jane Smith"})
    response = client.get("/users")
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_products():
    response = client.get("/products")
    assert response.status_code == 200
    assert len(response.json()) == 3 

def test_add_user_products():
    client.post("/users", json={"id": 3, "name": "Alice"})
    response = client.post("/users/3/products", json={"user_id": 3, "product_ids": [1, 2]})
    assert response.status_code == 200
    assert len(response.json()) == 2

def test_get_user_products():
    client.post("/users", json={"id": 4, "name": "Bob"})
    client.post("/users/4/products", json={"user_id": 4, "product_ids": [3]})
    response = client.get("/users/4/products")
    assert response.status_code == 200
    assert len(response.json()) == 1
