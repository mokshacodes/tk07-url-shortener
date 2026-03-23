"""Application configuration settings."""

from dataclasses import dataclass
from typing import Annotated, TypeAlias

from fastapi import Depends


@dataclass(frozen=True)
class Config:
    """Defines configuration values for the application.

    Attributes:
        links_path: Path to the JSON file that stores link data.
    """

    links_path: str = "data/links.json"


def config_factory() -> Config:
    return Config()


ConfigDI: TypeAlias = Annotated[Config, Depends(config_factory)]
"""Dependency-injected Config type."""
