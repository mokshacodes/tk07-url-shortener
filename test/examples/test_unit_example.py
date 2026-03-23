"""Example unit test.

Unit tests should avoid network calls and external services.
"""

from fastapi.routing import APIRouter

from routes.router import router


def test_router_is_apirouter() -> None:
    assert isinstance(router, APIRouter)
