"""Example integration test using pytest markers."""

from fastapi.testclient import TestClient
from pytest import mark

from main import app


@mark.integration
def test_openapi_available() -> None:
    client = TestClient(app)
    response = client.get("/openapi.json")
    assert response.status_code == 200
