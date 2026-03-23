"""FastAPI application entrypoint."""

from fastapi import FastAPI

from routes import router as api_router

app = FastAPI(
    title="TK06 API Design",
    contact={
        "name": "Kris Jordan",
        "url": "https://github.com/comp423-26s/tk05-KrisJordan.git",
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
)
app.include_router(api_router)
