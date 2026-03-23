## Project Overview

- **Language Runtime:** Python 3.14 (dev container)
- **Dependency manager:** `uv`
- **Web framework:** FastAPI (served with `uvicorn`)
- **Persistence:** The project will ultimately `SQLModel` for an ORM.
- **QA tools:** `ruff`, `pyright`, `pytest`, `pytest-cov`

## Repository Structure

- **Architectural Design Records:** [docs/arch/](docs/arch/)
- **Source code:** [src/](src/)
    - **Application entrypoint:** [src/main.py](src/main.py)
    - **Configuration:** [src/config.py](src/config.py)
    - **Database scaffolding:** [src/db.py](src/db.py)
    - **Persistence entities:** [src/entities/](src/entities/)
    - **API models:** [src/models/](src/models/)
    - **Routes:** [src/routes/](src/routes/)
    - **Services:** [src/services/](src/services/)
    - **Temporary file-backed store:** [src/store/](src/store/)
    - **Utility scripts:** [src/util/](src/util/)
- **Project scripts:** [scripts/](scripts/)
- **Tests:** [test/](test/)

## Architectural Expectations

- Keep the separation of concerns clear:
    - `src/models` for request/response and API-facing validation models.
    - `src/entities` for persistence-oriented `SQLModel` table definitions.
    - `src/services` for business logic.
    - `src/routes` for HTTP concerns.
- Prefer changes that preserve public HTTP behavior unless a task explicitly requires an API change.

## Automated QA Tooling

- Unit tests: `uv run pytest`
- Integration tests: `uv run pytest --integration`
- Test coverage: `uv run pytest --cov=src --cov-report=term-missing`
- Type check: `uv run pyright --project pyproject.toml`
- Format: `uv run ruff format .`
- Auto-fix safe linting issues: `uv run ruff check --fix .`
- Lint without fixing: `uv run ruff check .`
- QA script has all automated checks: `./scripts/run-qa.sh`

## Development Conventions

- Use Google-style Python documentation standards with simple, direct language.
- Follow existing module organization in `src/`.
- Keep public APIs stable unless the change request explicitly allows it.
- Prefer small, focused edits and avoid reformatting unrelated code.
- Update or add tests for changed or added behavior.
- Unit tests are in the test files whose names end with `_unit.py`. Integration tests end with `_integration.py`.
- Unit tests must be fully isolated from dependencies.
- Integration tests are marked with `@pytest.mark.integration`.
- 100% test coverage of code in the `src/` directory is required.
- When working on persistence changes, favor incremental migration from `src/store` toward `src/db.py` and `src/entities` rather than mixing database code into routes.

## Agent Conventions

- Source the virtual environment `.venv` when running terminal commands.
- Create step-by-step plan before making any changes.
- Do not add any dependencies unless specifically asked. Document any new dependency choice.
- Keep the starter-project teaching context in mind; prefer clear code over clever abstractions.
- Before completing a task always run `./scripts/run-qa.sh` as the final step. If issues arise in the QA tests, try to understand and explain why before asking the user if they would like you to attempt to fix the issue for them.
