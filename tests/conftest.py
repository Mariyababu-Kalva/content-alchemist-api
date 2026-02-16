import pytest
from fastapi.testclient import TestClient
from backend.main import app

@pytest.fixture
def client():
    """Fixture to provide a TestClient for all tests."""
    return TestClient(app)