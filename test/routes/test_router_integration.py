"""Integration tests for the follow_link route."""

from collections.abc import Iterator
from unittest.mock import MagicMock

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from main import app
from store.json_file_io import JSONFileIO
from store.link_store import LinkStore
from store.link_store_factory import link_store_factory


@pytest.fixture
def client_with_mocked_storage() -> Iterator[tuple[TestClient, MagicMock]]:
    """Provide a client wired to a mocked JSONFileIO dependency."""
    mock_storage = MagicMock(spec=JSONFileIO)

    def _override_link_store_factory() -> LinkStore:
        return LinkStore(mock_storage)

    app.dependency_overrides[link_store_factory] = _override_link_store_factory
    with TestClient(app) as client:
        yield client, mock_storage
    app.dependency_overrides.clear()


@pytest.mark.integration
def test_follow_link_redirects(
    client_with_mocked_storage: tuple[TestClient, MagicMock],
) -> None:
    """Redirects when a matching slug exists."""
    client, mock_storage = client_with_mocked_storage
    mock_storage.load.return_value = {
        "comp423": {"slug": "comp423", "target": "https://example.com"}
    }

    response = client.get("/comp423", follow_redirects=False)

    assert response.status_code is status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "https://comp423-26s.github.io"


@pytest.mark.integration
def test_follow_link_returns_404(
    client_with_mocked_storage: tuple[TestClient, MagicMock],
) -> None:
    """Returns 404 when the slug is missing."""
    client, mock_storage = client_with_mocked_storage
    mock_storage.load.return_value = {}

    response = client.get("/missing", follow_redirects=False)

    assert response.status_code is status.HTTP_404_NOT_FOUND
    assert response.text == "Not Found"
