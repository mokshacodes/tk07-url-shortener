"""Integration tests for the follow_link route."""

from collections.abc import Iterator
from pathlib import Path

import pytest
from fastapi import status
from fastapi.testclient import TestClient

from config import Config, config_factory
from main import app


@pytest.fixture
def client_with_temp_storage(tmp_path: Path) -> Iterator[tuple[TestClient, Path]]:
    """Provide a client and a temporary path for a data file."""

    data_file = tmp_path / "links.json"

    def _config_override() -> Config:
        return Config(links_path=str(data_file.absolute()))

    app.dependency_overrides[config_factory] = _config_override
    with TestClient(app) as client:
        yield (client, data_file)
    app.dependency_overrides.clear()


@pytest.mark.integration
def test_follow_link_redirects(
    client_with_temp_storage: tuple[TestClient, Path],
) -> None:
    """Redirects when a matching slug exists."""
    # Arrange
    client, data_path = client_with_temp_storage
    data_path.write_text(
        '{"comp423": {"slug": "comp423", "target": "https://github.com/comp423-26s"}}'
    )

    # Act
    response = client.get("/comp423", follow_redirects=False)

    # Assert
    assert response.status_code is status.HTTP_307_TEMPORARY_REDIRECT
    assert response.headers["location"] == "https://comp423-26s.github.io"


@pytest.mark.integration
def test_follow_link_returns_404(
    client_with_temp_storage: tuple[TestClient, Path],
) -> None:
    """Returns 404 when the slug is missing."""
    client, _ = client_with_temp_storage

    response = client.get("/missing", follow_redirects=False)

    assert response.status_code is status.HTTP_404_NOT_FOUND
    assert response.text == "Not Found"


@pytest.mark.integration
def test_create_and_list_links_e2e(
    client_with_temp_storage: tuple[TestClient, Path],
) -> None:
    """Creates a link and then lists it through the public API."""
    # Arrange
    client, _ = client_with_temp_storage

    # Act
    create_response = client.post(
        "/links",
        json={
            "slug": "comp423",
            "target": "https://github.com/comp423-26s",
        },
    )
    list_response = client.get("/links")

    # Assert
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
