"""Dependency injection helpers for the link service."""

from typing import Annotated, TypeAlias

from fastapi import Depends

from db import SessionDI

from .link_service import LinkService


def link_service_factory(session: SessionDI) -> LinkService:
    """Create a request-scoped link service."""
    return LinkService(session)


LinkServiceDI: TypeAlias = Annotated[LinkService, Depends(link_service_factory)]
