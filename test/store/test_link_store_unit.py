"""Unit tests for LinkStore without disk operations."""

from unittest.mock import MagicMock

from models import LinkModel
from store.json_file_io import JSONFileIO
from store.link_store import LinkStore


def test_get_returns_link_when_slug_exists() -> None:
    """Test that get returns the correct link for an existing slug."""

    # Arrange
    mock_storage = MagicMock(spec=JSONFileIO)
    mock_storage.load.return_value = {
        "example": {"slug": "example", "target": "https://example.com"},
        "github": {"slug": "github", "target": "https://github.com"},
    }

    # Act
    store = LinkStore(storage=mock_storage)
    result = store.get("example")

    # Assert
    assert result is not None
    assert result.slug == "example"
    assert result.target == "https://example.com"
    mock_storage.load.assert_called_once()


def test_get_returns_none_when_slug_not_found() -> None:
    """Test that get returns None for a non-existent slug."""

    # Arrange
    mock_storage = MagicMock(spec=JSONFileIO)
    mock_storage.load.return_value = None

    # Act
    store = LinkStore(storage=mock_storage)
    result = store.get("nonexistent")

    # Assert
    assert result is None
    mock_storage.load.assert_called_once()


def test_list_returns_all_links_without_mutation() -> None:
    """Test that list returns all links and does not expose internal state."""

    # Arrange
    mock_storage = MagicMock(spec=JSONFileIO)
    mock_storage.load.return_value = {
        "example": {"slug": "example", "target": "https://example.com"},
        "github": {"slug": "github", "target": "https://github.com"},
    }
    store = LinkStore(storage=mock_storage)

    # Act
    result = store.list()
    result.pop("example")

    # Assert
    assert set(result.keys()) == {"github"}
    assert set(store.list().keys()) == {"example", "github"}
    mock_storage.load.assert_called_once()


def test_put_stores_link_and_persists() -> None:
    """Test that put stores a link and persists updated data."""

    # Arrange
    mock_storage = MagicMock(spec=JSONFileIO)
    mock_storage.load.return_value = None
    store = LinkStore(storage=mock_storage)
    link = LinkModel(slug="example", target="https://example.com")

    # Act
    store.put("example", link)

    # Assert
    stored = store.get("example")
    assert stored == link
    mock_storage.persist.assert_called_once_with({"example": link.model_dump()})


def test_delete_removes_link_and_persists() -> None:
    """Test that delete removes a link and persists updated data."""

    # Arrange
    mock_storage = MagicMock(spec=JSONFileIO)
    mock_storage.load.return_value = {
        "example": {"slug": "example", "target": "https://example.com"},
        "github": {"slug": "github", "target": "https://github.com"},
    }
    store = LinkStore(storage=mock_storage)

    # Act
    store.delete("example")

    # Assert
    assert store.get("example") is None
    assert set(store.list().keys()) == {"github"}
    mock_storage.persist.assert_called_once_with(
        {"github": LinkModel(slug="github", target="https://github.com").model_dump()}
    )


def test_delete_missing_slug_is_noop() -> None:
    """Test that delete does nothing when slug is missing."""

    # Arrange
    mock_storage = MagicMock(spec=JSONFileIO)
    mock_storage.load.return_value = {
        "example": {"slug": "example", "target": "https://example.com"}
    }
    store = LinkStore(storage=mock_storage)

    # Act
    store.delete("missing")

    # Assert
    assert set(store.list().keys()) == {"example"}
    mock_storage.persist.assert_not_called()
