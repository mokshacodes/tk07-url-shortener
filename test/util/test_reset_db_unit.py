"""Unit tests for the database reset script."""

import runpy
from unittest.mock import MagicMock, patch

import pytest

from entities import Link
from util import reset_db


def test_ensure_databases_exist_creates_missing_databases(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Creates only databases that do not already exist."""
    # Arrange
    expected_admin_url = reset_db.POSTGRES_URL.rsplit("/", 1)[0] + "/postgres"
    admin_engine = MagicMock()
    conn = MagicMock()
    admin_engine.connect.return_value.__enter__.return_value = conn

    missing_db_result = MagicMock()
    missing_db_result.fetchone.return_value = None

    create_db_result = MagicMock()

    existing_db_result = MagicMock()
    existing_db_result.fetchone.return_value = object()

    conn.execute.side_effect = [
        missing_db_result,
        create_db_result,
        existing_db_result,
    ]

    # Act
    with patch(
        "util.reset_db.create_engine", return_value=admin_engine
    ) as mock_create_engine:
        reset_db.ensure_databases_exist()

    # Assert
    mock_create_engine.assert_called_once_with(
        expected_admin_url,
        isolation_level="AUTOCOMMIT",
        echo=False,
    )

    execute_calls = conn.execute.call_args_list
    assert len(execute_calls) == 3
    assert (
        str(execute_calls[0].args[0])
        == "SELECT 1 FROM pg_database WHERE datname = :name"
    )
    assert execute_calls[0].args[1] == {"name": "links_db"}
    assert str(execute_calls[1].args[0]) == "CREATE DATABASE links_db"
    assert (
        str(execute_calls[2].args[0])
        == "SELECT 1 FROM pg_database WHERE datname = :name"
    )
    assert execute_calls[2].args[1] == {"name": "links_db_test"}

    admin_engine.dispose.assert_called_once_with()

    captured = capsys.readouterr()
    assert "Created database 'links_db'" in captured.out
    assert "Database 'links_db_test' already exists" in captured.out


def test_reset_recreates_schema_and_seeds_links(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """Drops, recreates, and seeds the database with demo links."""
    # Arrange
    session = MagicMock()
    session_context = MagicMock()
    session_context.__enter__.return_value = session

    with (
        patch("util.reset_db.ensure_databases_exist") as mock_ensure_databases_exist,
        patch("util.reset_db.drop_db_and_tables") as mock_drop_db_and_tables,
        patch("util.reset_db.create_db_and_tables") as mock_create_db_and_tables,
        patch(
            "util.reset_db.Session", return_value=session_context
        ) as mock_session_cls,
    ):
        # Act
        reset_db.reset()

    # Assert
    mock_ensure_databases_exist.assert_called_once_with()
    mock_drop_db_and_tables.assert_called_once_with()
    mock_create_db_and_tables.assert_called_once_with()
    mock_session_cls.assert_called_once_with(reset_db.engine)

    seeded_links = session.add_all.call_args.args[0]
    assert len(seeded_links) == 2
    assert all(isinstance(link, Link) for link in seeded_links)
    assert [(link.slug, link.target, link.hits) for link in seeded_links] == [
        ("unc", "https://www.unc.edu", 0),
        ("423", "https://comp423-26s.github.io", 0),
    ]
    session.commit.assert_called_once_with()

    captured = capsys.readouterr()
    assert "→ Ensuring databases exist …" in captured.out
    assert "→ Dropping existing tables …" in captured.out
    assert "→ Creating tables …" in captured.out
    assert "→ Seeding accounts …" in captured.out
    assert "✓ Database reset complete." in captured.out


def test_main_guard_runs_reset_script() -> None:
    """Executes the reset workflow when the module runs as a script."""
    # Arrange
    admin_engine = MagicMock()
    conn = MagicMock()
    admin_engine.connect.return_value.__enter__.return_value = conn

    first_database_result = MagicMock()
    first_database_result.fetchone.return_value = object()
    second_database_result = MagicMock()
    second_database_result.fetchone.return_value = object()
    conn.execute.side_effect = [first_database_result, second_database_result]

    session = MagicMock()
    session_context = MagicMock()
    session_context.__enter__.return_value = session

    with (
        patch("sqlmodel.create_engine", return_value=admin_engine),
        patch("sqlmodel.Session", return_value=session_context),
        patch("db.drop_db_and_tables") as mock_drop_db_and_tables,
        patch("db.create_db_and_tables") as mock_create_db_and_tables,
        patch("db.engine", new=MagicMock()),
    ):
        # Act
        runpy.run_path("/workspace/src/util/reset_db.py", run_name="__main__")

    # Assert
    mock_drop_db_and_tables.assert_called_once_with()
    mock_create_db_and_tables.assert_called_once_with()
    session.add_all.assert_called_once_with(session.add_all.call_args.args[0])
    session.commit.assert_called_once_with()
