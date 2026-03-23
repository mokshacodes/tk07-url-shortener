# ADR006: Pivot Project

## Context

As recent events have shown, weather forecasting is very challenging. Third party weather APIs are also flaky. Thus, we need to pivot to an app we are capable of building and understanding in a few weeks. The application needs to be real enough to learn key lessons in software engineering from, but not overwhelming.

## Decision

We will build a URL shortening service. Eventually, we may add agentic AI features to the URL shortening service to differentiate it from services like bit.ly, or go.unc.edu, but, for now, we will aim to reproduce an old classic web application.

This will serve as a nice, contained example for software engineering practices in 2026. The service will have very few models and API end-points.

Our project's primary packages and directory structure will be:

- `src/models` - Where our Pydantic models will go
- `src/store` - Where our persistence layer is defined
- `src/services` - Where our business logic lives
- `src/routes` - Where our HTTP API will be defined in FastAPI
- `src/main.py` - Our entry-point to the FastAPI server that mounts our routes.

We need to take on three new production dependencies: `pydantic` for models, `fastapi` for routes, and `uvicorn` for web application serving. We need to remove the old dependency for `requests`.

We need to follow a convention of each module containing one class or groups of related functions with an appropriate name.

We need a script named `scripts/run-dev-server.sh` that will start the development server in live reload mode.

## Considered Options

- Claude Code Lite
	- Pros: the current meta.
	- Cons: more moving parts, complexity, and reliance on an LLM engine

- Todo List
	- Pros: the hello world of web development.
	- Cons: does not have interesting uses of HTTP responses (like redirects)

## Consequences

- We will delete our implementation and test code for our little weather CLI app
- We will need to start from scratch and reorganize our project
