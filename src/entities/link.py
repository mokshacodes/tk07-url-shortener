"""Pydantic model for shortened links."""

from sqlmodel import Field, SQLModel


class Link(SQLModel, table=True):
    """Represents a shortened link.

    Attributes:
        slug: Short identifier for the link.
        target: Destination URL for the link.
        hits: Hit count.
    """

    slug: str = Field(primary_key=True)
    target: str = Field(min_length=8)
    hits: int = Field(default=0)
