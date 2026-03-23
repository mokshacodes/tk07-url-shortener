from unittest.mock import MagicMock

import pytest

from models import LinkModel
from services import LinkService
from store import LinkStore


@pytest.fixture()
def link_svc() -> tuple[LinkService, MagicMock]:
    mock_store = MagicMock(spec=LinkStore)
    link_svc = LinkService(mock_store)
    return (link_svc, mock_store)


def test_link_service_get(link_svc: tuple[LinkService, MagicMock]):
    # Arrange
    svc, store_mock = link_svc
    expected: LinkModel = LinkModel(slug="423", target="https://comp423")
    store_mock.get.return_value = expected

    # Act
    actual = svc.get("423")

    # Assert
    assert actual is not None
    assert actual is expected
    assert actual.hits == 1
    store_mock.put.assert_called_once_with("423", expected)


def test_link_service_get_returns_none_for_missing_slug(
    link_svc: tuple[LinkService, MagicMock],
) -> None:
    # Arrange
    svc, store_mock = link_svc
    store_mock.get.return_value = None

    # Act
    actual = svc.get("missing")

    # Assert
    assert actual is None
    store_mock.put.assert_not_called()


def test_link_service_create_persists_new_link(
    link_svc: tuple[LinkService, MagicMock],
) -> None:
    # Arrange
    svc, store_mock = link_svc
    link = LinkModel(slug="423", target="https://comp423")
    store_mock.get.return_value = None

    # Act
    actual = svc.create("423", link)

    # Assert
    assert actual is link
    store_mock.get.assert_called_once_with("423")
    store_mock.put.assert_called_once_with("423", link)


def test_link_service_create_raises_for_duplicate_slug(
    link_svc: tuple[LinkService, MagicMock],
) -> None:
    # Arrange
    svc, _ = link_svc
    existing = LinkModel(slug="423", target="https://comp423")
    svc.get = MagicMock(return_value=existing)

    # Act / Assert
    with pytest.raises(ValueError, match="Slug `423` already taken."):
        svc.create("423", existing)


def test_link_service_list_links_returns_all_values(
    link_svc: tuple[LinkService, MagicMock],
) -> None:
    # Arrange
    svc, store_mock = link_svc
    comp423 = LinkModel(slug="423", target="https://comp423")
    unc = LinkModel(slug="unc", target="https://www.unc.edu")
    store_mock.list.return_value = {"423": comp423, "unc": unc}

    # Act
    actual = svc.list_links()

    # Assert
    assert actual == [comp423, unc]
