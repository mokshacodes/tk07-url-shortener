"""Link service utilities backed by a SQLModel session."""

from sqlmodel import Session, select

from entities import Link
from models import LinkModel


class LinkService:
    """Business logic around shortened links."""

    def __init__(self, session: Session):
        """Construct a service around a database session."""
        self._session = session

    def create(self, slug: str, link: LinkModel) -> LinkModel:
        """Create and persist a new shortened link."""
        existing = self._session.get(Link, slug)
        if existing is not None:
            raise ValueError(f"Slug `{slug}` already taken.")

        new_link = Link(slug=slug, target=link.target, hits=link.hits)
        self._session.add(new_link)
        self._session.commit()
        self._session.refresh(new_link)
        return LinkModel.model_validate(new_link)

    def get(self, slug: str) -> LinkModel | None:
        """Retrieve a link by slug and increment its hit counter."""
        link = self._session.get(Link, slug)
        if link is None:
            return None

        link.hits += 1
        self._session.add(link)
        self._session.commit()
        self._session.refresh(link)
        return LinkModel.model_validate(link)

    def list_links(self) -> list[LinkModel]:
        """Return all stored links."""
        links = self._session.exec(select(Link)).all()
        return [LinkModel.model_validate(link) for link in links]
