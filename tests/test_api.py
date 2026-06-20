from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

API_TOKEN = "age-check-api-token-2026"

headers = {
    "Authorization": f"Bearer {API_TOKEN}"
}


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_version():
    response = client.get("/version")
    assert response.status_code == 200
    assert "version" in response.json()


def test_home():
    response = client.get("/")
    assert response.status_code == 200