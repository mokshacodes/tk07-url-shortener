"""Dependency factory for creating link store instances."""

from pathlib import Path
from typing import Annotated, TypeAlias

from fastapi import Depends

from config import ConfigDI

from .json_file_io import JSONFileIO
from .link_store import LinkStore


def link_store_factory(config: ConfigDI) -> LinkStore:
    """Create a LinkStore wired to the configured JSON storage.

    Args:
        config: Application config containing the storage path.

    Returns:
        A LinkStore backed by the JSON file storage implementation.
    """

    storage = JSONFileIO(Path(config.links_path))
    return LinkStore(storage)


LinkStoreDI: TypeAlias = Annotated[LinkStore, Depends(link_store_factory)]
"""Dependency-injected LinkStore type."""
