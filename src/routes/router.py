"""API router for the URL shortener."""

from typing import Annotated

from fastapi import APIRouter, Body, Path, status
from fastapi.responses import RedirectResponse, Response

from models import LinkModel
from services import LinkServiceDI

router = APIRouter()


@router.post(
    "/links",
    summary="Create a new shortened link",
    tags=["Sue"],
)
def create_link(
    link: Annotated[
        LinkModel,
        Body(
            description="Shortened link to create",
            openapi_examples={
                "COMP423": {
                    "summary": "Short Link to COMP423",
                    "description": "Sample link",
                    "value": {
                        "slug": "comp423",
                        "target": "https://github.com/comp423-26s",
                    },
                }
            },
        ),
    ],
    link_svc: LinkServiceDI,
) -> LinkModel:
    """Create a new shortened link."""
    return link_svc.create(link.slug, link)


@router.get("/links", summary="List all Links", tags=["Amy"])
def read_links(link_svc: LinkServiceDI) -> list[LinkModel]:
    """List all shortened links."""
    return link_svc.list_links()


@router.get(
    "/{slug}",
    summary="Navigate to a shortened URL",
    description="When a matching slug exists, redirects user to the target. Otherwise, 404",
    responses={
        307: {"description": "Temporary redirect"},
        404: {"description": "Not found"},
    },
    tags=["Cai"],
    status_code=status.HTTP_307_TEMPORARY_REDIRECT,
)
def follow_link(
    slug: Annotated[
        str,
        Path(
            description="Slug of shortened Link",
            openapi_examples={
                "COMP423": {
                    "summary": "Short Link to COMP423",
                    "description": "Sample Slug to COMP423 website",
                    "value": "comp423",
                },
                "Non-existing Slug": {
                    "summary": "Short Link 404",
                    "description": "Expects a 404",
                    "value": "this-will-404",
                },
            },
        ),
    ],
    link_svc: LinkServiceDI,
) -> Response:
    """Redirect to the stored target URL when the slug exists."""
    link = link_svc.get(slug)
    if link is not None:
        return RedirectResponse(
            url=link.target,
            status_code=status.HTTP_307_TEMPORARY_REDIRECT,
        )
    return Response("Not Found", status.HTTP_404_NOT_FOUND)
