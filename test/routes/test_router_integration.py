"""Integration tests for router behavior with a real database session."""

from collections.abc import Iterator
from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlmodel import Session, SQLModel, create_engine

import main
from db import get_session
from entities import Link
from main import app


@pytest.fixture
def client_with_database(
    monkeypatch: pytest.MonkeyPatch,
) -> Iterator[tuple[TestClient, Any]]:
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
        yield client, engine
    app.dependency_overrides.clear()


@pytest.mark.integration
def test_follow_link_redirects(
    client_with_database: tuple[TestClient, Any],
) -> None:
    """Redirects when a matching slug exists."""
    client, engine = client_with_database
    with Session(engine) as session:
        session.add(Link(slug="comp423", target="https://example.com"))
        session.commit()

    response = client.get("/comp423", follow_redirects=False)

    assert response.status_code is status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "https://example.com"


@pytest.mark.integration
def test_follow_link_returns_404(
    client_with_database: tuple[TestClient, Any],
) -> None:
    """Returns 404 when the slug is missing."""
    client, _ = client_with_database

    response = client.get("/missing", follow_redirects=False)

    assert response.status_code is status.HTTP_404_NOT_FOUND
    assert response.text == "Not Found"
