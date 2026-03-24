"""FastAPI application entrypoint."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from db import create_db_and_tables
from routes import router as api_router


@asynccontextmanager
async def lifespan(_: FastAPI) -> AsyncIterator[None]:
    """Create database tables when the application starts."""
    create_db_and_tables()
    yield


app = FastAPI(
    title="TK07 ORM Refactor",
    contact={
        "name": "Kris Jordan",
        "url": "https://github.com/comp423-26s/tk07-starter",
    },
    description="""
## Introduction

This API is for link shortening.
""",
    openapi_tags=[
        {"name": "Sue", "description": "Sue Sharer's API Endpoints"},
        {"name": "Cai", "description": "Cai Clicker's API Endpoints"},
        {"name": "Amy", "description": "Amy Admin's API Endpoints"},
    ],
    lifespan=lifespan,
)

app.include_router(api_router)
