"""Database reset and seed script.

Run from the workspace root::

    PYTHONPATH=src uv run python src/util/reset_db.py

What it does:

1. **Creates** the ``bank`` and ``bank_test`` PostgreSQL databases if they
   do not already exist.
2. **Drops** the ``activity`` and ``accounts`` tables (if they exist).
3. **Recreates** them using the SQLModel metadata that our entity classes
   register.
4. **Inserts** a small set of seed rows so there is data to experiment
   with immediately.

This script is useful during development.  In production you would use
Alembic migrations instead of dropping and recreating tables.
"""

from sqlalchemy import text
from sqlmodel import Session, create_engine

from db import POSTGRES_URL, create_db_and_tables, drop_db_and_tables, engine
from entities import Link

# ---------------------------------------------------------------------------
# Admin connection URL – points to the built-in ``postgres`` maintenance
# database so we can issue CREATE DATABASE outside of a transaction.
# ---------------------------------------------------------------------------
_ADMIN_URL = POSTGRES_URL.rsplit("/", 1)[0] + "/postgres"
_DATABASES = ("links_db", "links_db_test")


def ensure_databases_exist() -> None:  # pragma: no cover
    """Create the ``bank`` and ``bank_test`` databases if they do not exist.

    ``CREATE DATABASE`` cannot run inside a transaction, so we open an
    *autocommit* connection to the ``postgres`` maintenance database.
    """
    admin_engine = create_engine(_ADMIN_URL, isolation_level="AUTOCOMMIT", echo=False)
    with admin_engine.connect() as conn:
        for db_name in _DATABASES:
            row = conn.execute(
                text("SELECT 1 FROM pg_database WHERE datname = :name"),
                {"name": db_name},
            ).fetchone()
            if row is None:
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"→ Created database '{db_name}'")
            else:
                print(f"→ Database '{db_name}' already exists")
    admin_engine.dispose()


def reset() -> None:
    """Create databases, drop all tables, recreate the schema, and seed demo data."""

    # ------------------------------------------------------------------
    # 0. Ensure both databases exist
    # ------------------------------------------------------------------
    print("→ Ensuring databases exist …")
    ensure_databases_exist()

    # ------------------------------------------------------------------
    # 1. Drop everything and recreate
    # ------------------------------------------------------------------
    print("→ Dropping existing tables …")
    drop_db_and_tables()

    print("→ Creating tables …")
    create_db_and_tables()

    # ------------------------------------------------------------------
    # 2. Seed accounts
    # ------------------------------------------------------------------
    print("→ Seeding accounts …")
    unc = Link(slug="unc", target="https://www.unc.edu")
    comp423 = Link(slug="423", target="https://comp423-26s.github.io")

    with Session(engine) as session:
        session.add_all([unc, comp423])
        session.commit()

    print("✓ Database reset complete.")


if __name__ == "__main__":
    reset()
