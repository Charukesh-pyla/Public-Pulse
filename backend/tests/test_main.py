import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_root_endpoint():
    """Verifies that the API root endpoint responds successfully."""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "Welcome to the" in data["message"]
    assert data["status"] == "running"

def test_health_endpoint_offline():
    """
    Verifies that the health check endpoint correctly returns 503 
    Service Unavailable and lists databases as offline when Docker is down.
    """
    response = client.get("/health")
    assert response.status_code == 503
    data = response.json()
    assert data["status"] == "unhealthy"
    assert data["services"]["database"] == "offline"
    assert data["services"]["redis"] == "offline"
