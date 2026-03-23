"""Integration tests for LinkStore with file persistence."""

from pathlib import Path

import pytest

from models import LinkModel
from store.json_file_io import JSONFileIO
from store.link_store import LinkStore

# === TESTS ===


@pytest.fixture
def populated_store(tmp_path: Path) -> tuple[Path, LinkStore]:
    """Create a store backed by a file with pre-populated data."""
    data_file = tmp_path / "links_with_data.json"
    data_file.write_text(
        '{"unc": {"slug": "unc", "target": "https://www.unc.edu"}, '
        '"duke": {"slug": "duke", "target": "https://www.duke.edu"}}'
    )
    store = LinkStore(JSONFileIO(data_file))

    return data_file, store


@pytest.mark.integration
def test_link_get(populated_store: tuple[Path, LinkStore]) -> None:
    """Test storing and retrieving a link with file persistence."""
    # Arrange
    _, store = populated_store

    # Act
    retrieved = store.get("unc")

    # Assert
    assert retrieved is not None
    assert retrieved.slug == "unc"
    assert retrieved.target == "https://www.unc.edu"


@pytest.mark.integration
def test_link_get_new_file(tmp_path: Path) -> None:
    """Test storing and retrieving a link with file persistence."""
    # Arrange
    temp_store_file_new = JSONFileIO(tmp_path / "links.json")
    store = LinkStore(temp_store_file_new)

    # Act
    retrieved = store.get("unc")

    # Assert
    assert retrieved is None


@pytest.mark.integration
def test_link_list_persists_data(populated_store: tuple[Path, LinkStore]) -> None:
    """Test listing links loads existing file data."""
    # Arrange
    _, store = populated_store

    # Act
    listed = store.list()

    # Assert
    assert set(listed.keys()) == {"unc", "duke"}
    assert listed["unc"].target == "https://www.unc.edu"
    assert listed["duke"].target == "https://www.duke.edu"


@pytest.mark.integration
def test_link_put_persists_to_disk(tmp_path: Path) -> None:
    """Test storing a link persists the mutation to disk."""
    # Arrange
    data_file = tmp_path / "links.json"
    storage = JSONFileIO(data_file)
    store = LinkStore(storage)

    # Act
    store.put("unc", LinkModel(slug="unc", target="https://www.unc.edu"))
    reloaded = LinkStore(JSONFileIO(data_file)).get("unc")

    # Assert
    assert reloaded is not None
    assert reloaded.slug == "unc"
    assert reloaded.target == "https://www.unc.edu"


@pytest.mark.integration
def test_link_delete_persists_to_disk(populated_store: tuple[Path, LinkStore]) -> None:
    """Test deleting a link persists the mutation to disk."""
    # Arrange
    data_file, store = populated_store

    # Act
    store.delete("unc")
    reloaded = LinkStore(JSONFileIO(data_file)).list()

    # Assert
    assert "unc" not in reloaded
    assert set(reloaded.keys()) == {"duke"}
    assert reloaded["duke"].target == "https://www.duke.edu"
