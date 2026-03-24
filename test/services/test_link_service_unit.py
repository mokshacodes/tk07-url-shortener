"""Unit tests for the link service."""

from unittest.mock import MagicMock

import pytest
from sqlmodel import Session

from entities import Link
from models import LinkModel
from services import LinkService


@pytest.fixture()
def session_mock() -> MagicMock:
    """Provide a mocked database session."""
    return MagicMock(spec=Session)


@pytest.fixture()
def link_svc(session_mock: MagicMock) -> LinkService:
    """Provide a link service wired to a mocked session."""
    return LinkService(session_mock)


def test_link_service_get(session_mock: MagicMock, link_svc: LinkService) -> None:
    """Returns a link model and increments its hit count."""
    existing = Link(slug="423", target="https://comp423", hits=0)
    session_mock.get.return_value = existing

    actual = link_svc.get("423")

    assert actual == LinkModel(slug="423", target="https://comp423", hits=1)
    session_mock.get.assert_called_once_with(Link, "423")
    session_mock.add.assert_called_once_with(existing)
    session_mock.commit.assert_called_once_with()
    session_mock.refresh.assert_called_once_with(existing)


def test_link_service_get_returns_none_for_missing_slug(
    session_mock: MagicMock, link_svc: LinkService
) -> None:
    """Returns None when the slug does not exist."""
    session_mock.get.return_value = None

    actual = link_svc.get("missing")

    assert actual is None
    session_mock.add.assert_not_called()
    session_mock.commit.assert_not_called()
    session_mock.refresh.assert_not_called()


def test_link_service_create_persists_new_link(
    session_mock: MagicMock, link_svc: LinkService
) -> None:
    """Persists a new link and returns it."""
    session_mock.get.return_value = None
    link = LinkModel(slug="423", target="https://comp423")

    actual = link_svc.create("423", link)

    assert actual == LinkModel(slug="423", target="https://comp423", hits=0)
    session_mock.get.assert_called_once_with(Link, "423")
    added_link = session_mock.add.call_args.args[0]
    assert isinstance(added_link, Link)
    assert (added_link.slug, added_link.target, added_link.hits) == (
        "423",
        "https://comp423",
        0,
    )
    session_mock.commit.assert_called_once_with()
    session_mock.refresh.assert_called_once_with(added_link)


def test_link_service_create_raises_for_duplicate_slug(
    session_mock: MagicMock, link_svc: LinkService
) -> None:
    """Raises ValueError for duplicate slugs."""
    existing = Link(slug="423", target="https://comp423")
    session_mock.get.return_value = existing

    with pytest.raises(ValueError, match="Slug `423` already taken."):
        link_svc.create("423", LinkModel(slug="423", target="https://comp423"))

    session_mock.add.assert_not_called()
    session_mock.commit.assert_not_called()


def test_link_service_list_links_returns_all_values(
    session_mock: MagicMock, link_svc: LinkService
) -> None:
    """Returns all stored links as link models."""
    comp423 = Link(slug="423", target="https://comp423")
    unc = Link(slug="unc", target="https://www.unc.edu")
    exec_result = MagicMock()
    exec_result.all.return_value = [comp423, unc]
    session_mock.exec.return_value = exec_result

    actual = link_svc.list_links()

    assert actual == [
        LinkModel(slug="423", target="https://comp423", hits=0),
        LinkModel(slug="unc", target="https://www.unc.edu", hits=0),
    ]
    session_mock.exec.assert_called_once()
