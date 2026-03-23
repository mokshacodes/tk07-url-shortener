# ADR004: Use `ruff` for Linting and Formatting

## Context

We want consistent code style and early feedback on common errors (unused imports, undefined names, accidental shadowing, unsafe patterns) without slowing down the tight developer feedback loops established by ADR01 (`uv`) and ADR00 (Dev Container).

The linting/formatting tool we choose should:

- Be fast enough to run on every save and in CI.
- Provide high-signal, actionable diagnostics with automatic fixes where safe.
- Cover both formatting and a broad set of lint rules with minimal tool sprawl.
- Centralize configuration in `pyproject.toml` to reduce project configuration surface area.
- Integrate well with IDEs (VS Code) and common CI environments.

We do not need a complex publishing-oriented toolchain; we prefer minimal, pragmatic tooling that reduces maintenance overhead.

## Decision

Adopt `ruff` as the primary linter and formatter for this repository.

Rationale:

- `ruff` is extremely fast (implemented in Rust) and is therefore well-suited to run frequently (on-save locally and on every CI run).
- `ruff format` provides a consistent formatter without requiring a separate tool, keeping the workflow simple.
- `ruff check` consolidates many common lint rules (including import sorting and a large ecosystem of rule sets) into one tool, reducing dependency footprint and configuration overhead.
- Configuration lives in `pyproject.toml`, aligning with the project’s “minimal config” approach.

Project conventions implied by this decision:

- Linting and formatting are both enforced by `ruff`.
- Configuration lives in `pyproject.toml` under `[tool.ruff]`.
- Developers can run formatting and lint fixes locally, and CI can enforce a clean, repeatable standard.

## Considered Options

- `flake8` + `black` + `isort`:
	- Pros: widely used; clear separation of concerns; lots of plugins.
	- Cons: multiple tools and config surfaces; slower overall feedback loop; version and plugin interactions can add maintenance overhead.

- `pylint`:
	- Pros: deep, opinionated analysis; catches some issues other linters may miss.
	- Cons: higher noise/false positives for many teams; heavier configuration and tuning; slower than `ruff` for common workflows.

- `autopep8` / `yapf` (formatters):
	- Pros: automatic formatting available.
	- Cons: does not address the broader linting needs; still requires separate lint tooling; less alignment with a single consolidated toolchain.

- `pre-commit` as the primary enforcement mechanism:
	- Pros: great developer UX for consistent local checks.
	- Cons: it is an orchestrator, not a linter/formatter; we can add it later if desired, but it doesn’t replace choosing the underlying tools.

## Consequences

- Faster iteration: `ruff`’s speed supports frequent local checks and short CI cycles.
- Reduced tool sprawl: a single primary tool replaces a multi-tool lint/format stack in many cases.
- Centralized configuration: fewer files and less cognitive load when changing rules.
- Some convention and tuning required: teams must agree on a baseline ruleset and evolve it deliberately to avoid churn.
- Scope boundaries: `ruff` is not a type checker; static typing (e.g., via `mypy`/`pyright`) can be added later if the project needs it.