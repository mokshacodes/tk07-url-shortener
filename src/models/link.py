"""API-facing Pydantic model for shortened links."""

from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field


class LinkModel(BaseModel):
    """Represents a shortened link.

    Attributes:
        slug: Short identifier for the link.
        target: Destination URL for the link.
        hits: Hit count for the link.
    """

    model_config = ConfigDict(from_attributes=True)

    slug: Annotated[str, Field(frozen=True, min_length=3)]
    target: Annotated[str, Field(frozen=True, min_length=8)]
    hits: Annotated[int, Field(ge=0)] = 0
