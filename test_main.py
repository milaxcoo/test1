from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_get_all_traffic():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_traffic_by_customer_name():
    response = client.get("/", params={"customer_name": "John Doe"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]['customer_name'] == "John Doe"

def test_no_data_found():
    response = client.get("/", params={"customer_name": "Nonexistent User"})
    assert response.status_code == 404
    assert response.json()['detail'] == "Данные не найдены"
