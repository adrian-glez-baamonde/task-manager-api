from fastapi.testclient import TestClient
from app.main import app


client = TestClient(app)


def test_create_category_success():
    response = client.post("/categories", json={"name": "Trabajo"})
    assert response.status_code == 200

    data = response.json()
    assert data["name"] == "Trabajo"

    assert "id" in data


def test_create_category_missing_name():
    response = client.post("/categories", json={})
    assert response.status_code == 422


def test_get_all_categories():
    response_create = client.post("/categories", json={"name": "Trabajo"})
    created_category = response_create.json()

    response = client.get("/categories")
    assert response.status_code == 200
    
    data = response.json()
    assert any(category["id"] == created_category["id"] for category in data)