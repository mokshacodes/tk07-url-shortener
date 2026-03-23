"""Link service utilities.

This module provides the `LinkService` class which implements business
logic for creating, retrieving, and listing shortened links using a
backing link store (injected via `LinkStoreDI`).
"""

from models import LinkModel
from store import LinkStoreDI


class LinkService:
    """Business logic around shortened links.

    Attributes:
        _link_store (LinkStoreDI): The storage backend implementing the
            `LinkStoreDI` interface used to persist `Link` instances.
    """

    def __init__(self, link_store: LinkStoreDI):
        """Constructor.

        Args:
            link_store: A concrete implementation of `LinkStoreDI` used to
                store and retrieve `Link` objects.
        """
        self._link_store = link_store

    def create(self, slug: str, link: LinkModel) -> LinkModel:
        """Create and persist a new shortened link.

        Args:
            slug: The short identifier to register for the link.
            link: The :class:`Link` object to associate with `slug`.

        Returns:
            The same :class:`Link` instance that was stored.

        Raises:
            ValueError: If the provided `slug` is already taken.
        """
        if self.get(slug) is None:
            self._link_store.put(slug, link)
            return link
        else:
            raise ValueError(f"Slug `{slug}` already taken.")

    def get(self, slug: str) -> LinkModel | None:
        """Retrieve a link by slug and increment its hit counter.

        Args:
            slug: The short identifier for the link to retrieve.

        Returns:
            The stored :class:`Link` if found, otherwise ``None``.
        """
        link = self._link_store.get(slug)
        if link:
            link.hits += 1
            self._link_store.put(slug, link)
        return link

    def list_links(self) -> list[LinkModel]:
        """Return a list of all stored links.

        Returns:
            A list of :class:`Link` instances currently stored.
        """
        return list(self._link_store.list().values())
