"""Unit tests for LinkStoreFactory without disk operations."""

from pathlib import Path
from unittest.mock import MagicMock, patch

from config import Config
from store import link_store_factory
from store.json_file_io import JSONFileIO
from store.link_store import LinkStore


def test_link_store_factory_builds_store_from_settings() -> None:
    """Builds a LinkStore using settings.links_path."""
    settings = Config(links_path="custom-links.json")
    mock_storage = MagicMock(spec=JSONFileIO)
    mock_store = MagicMock(spec=LinkStore)

    with (
        patch(
            "store.link_store_factory.JSONFileIO", return_value=mock_storage
        ) as mock_json_file_io_cls,
        patch(
            "store.link_store_factory.LinkStore", return_value=mock_store
        ) as mock_link_store_cls,
    ):
        result = link_store_factory.link_store_factory(settings)

    mock_json_file_io_cls.assert_called_once_with(Path("custom-links.json"))
    mock_link_store_cls.assert_called_once_with(mock_storage)
    assert result is mock_store
