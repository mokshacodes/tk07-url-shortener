from typing import Annotated, TypeAlias

from fastapi import Depends

from .link_service import LinkService

LinkServiceDI: TypeAlias = Annotated[LinkService, Depends()]
