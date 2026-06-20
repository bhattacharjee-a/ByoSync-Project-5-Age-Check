from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_health_without_token():
    response = client.get("/health")
    assert response.status_code == 200


def test_check_age_without_token():
    response = client.post("/check_age")
    assert response.status_code in [401, 403]


def test_admin_latest_without_token():
    response = client.get("/admin/latest")
    assert response.status_code in [401, 403]