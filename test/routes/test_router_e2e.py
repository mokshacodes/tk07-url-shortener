"""End-to-end tests for the public API."""

from collections.abc import Iterator

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import main
from db import get_session
from main import app


@pytest.fixture
def client_with_database(monkeypatch: pytest.MonkeyPatch) -> Iterator[TestClient]:
    """Provide a client backed by an in-memory SQLite database."""
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    monkeypatch.setattr(main, "create_db_and_tables", lambda: None)

    def _override_get_session() -> Iterator[Session]:
        with Session(engine) as session:
            yield session

    app.dependency_overrides[get_session] = _override_get_session
    with TestClient(app) as client:
        yield client
    app.dependency_overrides.clear()


@pytest.mark.integration
def test_follow_link_redirects(client_with_database: TestClient) -> None:
    """Redirects when a matching slug exists."""
    create_response = client_with_database.post(
        "/links",
        json={
            "slug": "comp423",
            "target": "https://github.com/comp423-26s",
        },
    )

    response = client_with_database.get("/comp423", follow_redirects=False)

    assert create_response.status_code is status.HTTP_200_OK
    assert response.status_code is status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "https://github.com/comp423-26s"


@pytest.mark.integration
def test_follow_link_returns_404(client_with_database: TestClient) -> None:
    """Returns 404 when the slug is missing."""
    response = client_with_database.get("/missing", follow_redirects=False)

    assert response.status_code is status.HTTP_404_NOT_FOUND
    assert response.text == "Not Found"


@pytest.mark.integration
def test_create_and_list_links_e2e(client_with_database: TestClient) -> None:
    """Creates a link and then lists it through the public API."""
    create_response = client_with_database.post(
        "/links",
        json={
            "slug": "comp423",
            "target": "https://github.com/comp423-26s",
        },
    )
    list_response = client_with_database.get("/links")

    assert create_response.status_code is status.HTTP_200_OK
    assert create_response.json() == {
        "slug": "comp423",
        "target": "https://github.com/comp423-26s",
        "hits": 0,
    }
    assert list_response.status_code is status.HTTP_200_OK
    assert list_response.json() == [
        {
            "slug": "comp423",
            "target": "https://github.com/comp423-26s",
            "hits": 0,
        }
    ]
