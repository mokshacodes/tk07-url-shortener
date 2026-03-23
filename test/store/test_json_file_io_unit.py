"""Unit tests for JSONFileIO without disk operations."""

from pathlib import Path
from unittest.mock import MagicMock, mock_open, patch

from store.json_file_io import JSONFileIO


def test_load_returns_none_when_file_does_not_exist() -> None:
    """Test that load returns None when the file does not exist."""
    # Arrange
    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = False
    storage = JSONFileIO(data_path=mock_path)

    # Act
    result = storage.load()

    # Assert
    assert result is None
    mock_path.exists.assert_called_once()


def test_load_returns_data_from_file() -> None:
    """Test that load returns parsed JSON data from the file."""
    # Arrange
    mock_path = MagicMock(spec=Path)
    mock_path.exists.return_value = True
    test_data = {"key": "value", "number": 42}
    mock_file = mock_open(read_data='{"key": "value", "number": 42}')

    storage = JSONFileIO(data_path=mock_path)

    # Act
    with patch.object(mock_path, "open", mock_file):
        result = storage.load()

    # Assert
    assert result == test_data
    mock_path.exists.assert_called_once()
    mock_file.assert_called_once_with("r")


def test_persist_creates_parent_dir() -> None:
    """Test that persist ensures parent directories exist."""
    # Arrange
    mock_path = MagicMock(spec=Path)
    mock_parent = MagicMock(spec=Path)
    mock_path.parent = mock_parent
    storage = JSONFileIO(data_path=mock_path)

    # Act
    with (
        patch.object(mock_path, "open", mock_open()),
        patch("store.json_file_io.json.dump"),
    ):
        storage.persist({"key": "value"})

    # Assert
    mock_parent.mkdir.assert_called_once_with(parents=True, exist_ok=True)


def test_persist_writes_json_to_file() -> None:
    """Test that persist writes JSON to the file."""
    # Arrange
    mock_path = MagicMock(spec=Path)
    mock_path.parent = MagicMock(spec=Path)
    test_data = {"key": "value", "number": 42}
    mock_file = mock_open()
    storage = JSONFileIO(data_path=mock_path)

    # Act
    with (
        patch.object(mock_path, "open", mock_file) as mocked_open,
        patch("store.json_file_io.json.dump") as mock_dump,
    ):
        storage.persist(test_data)

    # Assert
    mocked_open.assert_called_once_with("w")
    mock_dump.assert_called_once_with(test_data, mock_file())
