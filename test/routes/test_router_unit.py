from unittest.mock import MagicMock

from fastapi import status
from fastapi.responses import RedirectResponse, Response

from models import LinkModel
from routes.router import create_link, follow_link, read_links
from services import LinkService


def test_follow_link() -> None:
    # Arrange
    slug = "423"
    link_svc = MagicMock(spec=LinkService)
    link_svc.get.return_value = LinkModel(
        slug="423", target="https://comp423-26s.github.io"
    )

    # Act
    result = follow_link(slug, link_svc)

    # Assert
    assert isinstance(result, RedirectResponse)
    assert result.status_code is status.HTTP_307_TEMPORARY_REDIRECT
    assert result.headers["Location"] == "https://comp423-26s.github.io"


def test_create_link_returns_payload() -> None:
    # Arrange
    link = LinkModel(slug="comp423", target="https://github.com/comp423-26s")
    link_svc = MagicMock(spec=LinkService)
    link_svc.create.return_value = link

    # Act
    result = create_link(link, link_svc)

    # Assert
    assert result == link


def test_read_links_returns_service_results() -> None:
    # Arrange
    comp423 = LinkModel(slug="comp423", target="https://github.com/comp423-26s")
    unc = LinkModel(slug="unc", target="https://www.unc.edu")
    link_svc = MagicMock(spec=LinkService)
    link_svc.list_links.return_value = [comp423, unc]

    # Act
    result = read_links(link_svc)

    # Assert
    assert result == [comp423, unc]


def test_follow_link_returns_not_found_response() -> None:
    # Arrange
    slug = "missing"
    link_svc = MagicMock(spec=LinkService)
    link_svc.get.return_value = None

    # Act
    result = follow_link(slug, link_svc)

    # Assert
    assert isinstance(result, Response)
    assert result.status_code == status.HTTP_404_NOT_FOUND
    assert result.body == b"Not Found"
