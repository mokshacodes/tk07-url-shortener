"""Database engine and session configuration.

This module centralises all database connectivity so that the rest of the
application never creates engines or sessions directly.  FastAPI route handlers
receive a ``Session`` via dependency injection (see ``SessionDI`` below).

Key concepts to understand in SQLAlchemy / SQLModel
------------------------------------------------------
* **Engine** – a long-lived object that manages a *pool* of raw database
  connections.  You typically create **one** engine per application process.
* **Session** – a short-lived "unit of work" that groups one or more SQL
  statements into a logical transaction.  You create a **new session per
  request** and close it when the request is done.
* **`yield` dependency** – FastAPI calls our generator, gives the yielded
  ``Session`` to the route handler, and then resumes the generator (which
  closes the session) after the response is sent.  This guarantees cleanup.
"""

from collections.abc import Generator
from typing import Annotated, TypeAlias

from fastapi import Depends
from sqlmodel import Session, SQLModel, create_engine

# ---------------------------------------------------------------------------
# Connection URL
# ---------------------------------------------------------------------------
# The hostname ``db`` matches the service name in docker-compose.yml.
# Docker Compose networking makes that hostname resolve to the Postgres
# container from within the ``app`` container.
#
# In a real application this connection string will NOT be hard coded! We will
# use configuration techniques to pull these values in from the environment.

POSTGRES_URL = "postgresql://postgres:password@db:5432/links_db"

# ---------------------------------------------------------------------------
# Engine (singleton – created once at import time)
# ---------------------------------------------------------------------------
# ``echo=True`` prints every SQL statement to stdout which is invaluable
# while learning.  Turn it off (``echo=False``) in production.

engine = create_engine(POSTGRES_URL, echo=True)

# ---------------------------------------------------------------------------
# Schema helpers
# ---------------------------------------------------------------------------


def create_db_and_tables() -> None:  # pragma: no cover
    """Create all registered tables if they do not already exist.

    All ``SQLModel`` entity classes (``table=True``) must be imported before
    calling this function so that they are registered with
    ``SQLModel.metadata``.  ``reset_db.py`` handles this by importing from
    ``entities`` at the top of the module.

    In a production app you would use Alembic migrations instead.
    """
    SQLModel.metadata.create_all(engine)


def drop_db_and_tables() -> None:  # pragma: no cover
    """Drop all registered tables.

    Same import requirement as ``create_db_and_tables`` – entity classes
    must be imported first so their metadata is registered.
    """
    SQLModel.metadata.drop_all(engine)


# ---------------------------------------------------------------------------
# Session dependency for FastAPI
# ---------------------------------------------------------------------------


def get_session() -> Generator[Session, None, None]:  # pragma: no cover
    """Provide a transactional database session for a single request.

    Usage in a route handler (via dependency injection)::

        @router.get("/items")
        def list_items(session: SessionDI):
            return session.exec(select(Item)).all()

    The session is automatically closed after the response is sent, even if
    an exception occurs, thanks to the `with` context manager.
    """
    with Session(engine) as session:
        yield session


# A convenience type alias so route handlers can write:
#     def my_route(session: SessionDI): ...
# instead of the more verbose:
#     def my_route(session: Annotated[Session, Depends(get_session)]): ...
SessionDI: TypeAlias = Annotated[Session, Depends(get_session)]
