"""File-backed store abstraction for shortened links."""

from typing import Optional

from models import LinkModel
from store.json_file_io import JSONFileIO


class LinkStore:
    """Stores and retrieves shortened links using a file-based data source.

    Attributes:
        _storage: JSON file I/O backend for persistence.
        _urls: Mapping of slug to stored link.
    """

    _storage: JSONFileIO
    _urls: dict[str, LinkModel]

    def __init__(self, storage: JSONFileIO):
        """Initialize the store.

        Args:
            storage: JSONFileIO instance for persistence.
        """
        self._storage = storage
        self._urls = self._load_data()

    def get(self, slug: str) -> Optional[LinkModel]:
        """Return the stored link for a slug.

        Args:
            slug: Short identifier for the link.

        Returns:
            The stored link, or None if not found.
        """
        return self._urls.get(slug, None)

    def put(self, slug: str, url: LinkModel) -> None:
        """Store or replace a link for a slug.

        Args:
            slug: Short identifier for the link.
            url: Link object to store and persist.
        """
        self._urls[slug] = url
        self._persist_data()

    def delete(self, slug: str) -> None:
        """Remove a stored link.

        Args:
            slug: Short identifier for the link.
        """
        if slug not in self._urls:
            return

        del self._urls[slug]
        self._persist_data()

    def list(self) -> dict[str, LinkModel]:
        """Return all stored links.

        Returns:
            Mapping of slug to stored link.
        """
        return self._urls.copy()

    def _load_data(self) -> dict[str, LinkModel]:
        """Load persisted links from disk if data path exists.

        Returns:
            Dictionary mapping slug to Link, empty if no data file exists.
        """
        data = self._storage.load()
        if data is None:
            return {}

        return {slug: LinkModel(**link_data) for slug, link_data in data.items()}

    def _persist_data(self) -> None:
        """Persist current links to disk."""
        self._storage.persist(
            {key: link.model_dump() for key, link in self._urls.items()}
        )
