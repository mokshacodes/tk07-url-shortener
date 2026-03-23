# URL Shortener Starter Project

This repository is a starter for a FastAPI-based URL shortener project used in a course setting. It is intentionally set up as a handoff point for students.

The current application works with a temporary file-backed persistence layer in [src/store](src/store). The next major student task is to replace that implementation with a real database persistence layer using `SQLModel`.

## Project Goals

- Provide a small but realistic FastAPI codebase.
- Demonstrate ADR-driven project setup.
- Separate HTTP routes, business logic, API models, and persistence concerns.
- Give students a clear migration path from a file-backed store to database-backed persistence.

## Current Architecture

The repository is organized around a simple layered design:

- [src/main.py](src/main.py): FastAPI application entrypoint.
- [src/routes](src/routes): HTTP endpoints and response behavior.
- [src/services](src/services): Business logic.
- [src/models](src/models): API-facing Pydantic models.
- [src/store](src/store): Current file-backed persistence layer.
- [src/entities](src/entities): `SQLModel` entity definitions for database-backed persistence work.
- [src/db.py](src/db.py): Database engine, session, and schema helpers.

## Student Handoff Notes

Students should treat this repository as a starting point, not a finished architecture.

The intended evolution is:

1. Keep the FastAPI routes working.
2. Preserve or improve the service-layer behavior.
3. Replace the file-backed store implementation in [src/store](src/store) with a real database-backed persistence layer.
4. Use `SQLModel` for entity modeling, schema creation, and session-based data access.

Where practical, request and response behavior should remain stable while persistence is being swapped out.

## ADRs

Architecture decisions for this starter live in [docs/arch](docs/arch). Important records include:

- [docs/arch/adr001-uv-for-dependency-management.md](docs/arch/adr001-uv-for-dependency-management.md)
- [docs/arch/adr002-pytest-for-automated-tests.md](docs/arch/adr002-pytest-for-automated-tests.md)
- [docs/arch/adr003-pyright-for-type-checking.md](docs/arch/adr003-pyright-for-type-checking.md)
- [docs/arch/adr004-ruff-for-linting-formatting.md](docs/arch/adr004-ruff-for-linting-formatting.md)
- [docs/arch/adr005-use-github-actions-for-ci.md](docs/arch/adr005-use-github-actions-for-ci.md)
- [docs/arch/adr006-url-shortener-pivot.md](docs/arch/adr006-url-shortener-pivot.md)
- [docs/arch/adr007-tag-integration-tests.md](docs/arch/adr007-tag-integration-tests.md)
- [docs/arch/adr008-use-sqlmodel-for-database-persistence.md](docs/arch/adr008-use-sqlmodel-for-database-persistence.md)

## Development Environment

- **Dev Container:** [.devcontainer/devcontainer.json](.devcontainer/devcontainer.json)
- **Runtime:** Python `3.14`
- **Dependency manager:** `uv`
- **Main framework:** FastAPI
- **Persistence target:** `SQLModel`

Open the repository in the provided dev container for a consistent setup.

## Install Dependencies

From the repository root:

```bash
uv sync --frozen
uv sync --group dev
```

## Run the Development Server

Start the application with the provided script:

```bash
./scripts/run-dev-server.sh
```

Once the server is running, open the forwarded port for `8000` and visit `/docs` for the OpenAPI UI.

## Testing

This project uses `pytest` for both unit and integration testing.

- Unit tests: `uv run pytest`
- Integration tests: `uv run pytest --integration`
- Coverage: `uv run pytest --cov=src --cov-report=term-missing`

## Type Checking

This project uses `pyright` in strict mode.

- Run type checking: `uv run pyright --project pyproject.toml`

## Linting and Formatting

This project uses `ruff` for formatting and linting.

- Format: `uv run ruff format .`
- Check lint: `uv run ruff check .`
- Auto-fix safe lint issues: `uv run ruff check --fix .`

## Run Full QA

Before handing off work, run the full QA script:

```bash
./scripts/run-qa.sh
```

This runs formatting, linting, type checking, unit tests, and the full test suite with coverage.
