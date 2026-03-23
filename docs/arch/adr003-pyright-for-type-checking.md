
# ADR003: Use `pyright` for Type Checking

## Context

We want early, high-signal feedback on type-related issues (mismatched return types, incorrect argument types, missing `None` handling, unsafe attribute access) without slowing down the tight developer feedback loops established by ADR00 (Dev Container) and ADR01 (`uv`).

Because we standardize on a Dev Container (ADR00), developers should get the same type-checking behavior across machines. Because we standardize on `uv` (ADR01), the type-checking tool should be installed and versioned as part of the project environment rather than relying on a globally-installed tool.

Our type-checking tool should:

- Be fast enough to run frequently (locally and in CI).
- Produce actionable diagnostics that match what developers see in VS Code.
- Support gradual typing: it should help us improve type coverage over time without forcing a “big bang” migration.
- Centralize configuration in `pyproject.toml` to reduce tool configuration surface area.
- Work well with modern Python features (type narrowing, `typing`/`collections.abc`, dataclasses) and common libraries.

Type checking is intentionally complementary to ADR004 (`ruff`): `ruff` handles linting/formatting, while a type checker validates type correctness.

## Decision

Adopt `pyright` as the primary type checker for this repository.

Rationale:

- `pyright` is fast and designed for tight feedback loops, which fits our dev-container-first workflow.
- VS Code’s Python experience (Pylance) is powered by the same underlying type analysis engine as `pyright`, so diagnostics in the editor align closely with command-line checks.
- `pyright` supports gradual adoption via configurable strictness and per-module/per-package overrides, letting us add type coverage iteratively.
- `pyright` can be installed and pinned as part of the project environment managed by `uv` (ADR01), supporting deterministic, repeatable checks.
- Configuration can live in `pyproject.toml`, keeping the project’s configuration surface area small and consistent with ADR004.

Project conventions implied by this decision:

- Type checking is performed with `pyright`.
- Configuration lives in `pyproject.toml` under `[tool.pyright]`.
- Types are added incrementally: new/changed code should prefer explicit type hints where practical.

## Considered Options

- `mypy`:
	- Pros: mature ecosystem; widely used; flexible configuration; lots of documentation.
	- Cons: typically slower than `pyright` for large iteration loops; editor diagnostics can diverge depending on plugins/settings; often requires more tuning to reach a similar developer experience.

- No type checking (linting + tests only):
	- Pros: minimal tooling; no additional configuration.
	- Cons: misses an entire class of issues that tests and linters often don’t catch (especially around `Optional`, protocol/interface mismatches, and refactors).

- `pytype`:
	- Pros: strong inference in some cases; can be valuable on specific codebases.
	- Cons: less aligned with the default VS Code Python experience; can be heavier to adopt and tune for day-to-day use.

## Consequences

- Earlier detection of type-related regressions, especially during refactors.
- More consistent IDE experience: the editor and CI can agree on type-checking results.
- `pyright` becomes part of our development toolchain and should be managed via `uv` to keep versions consistent across the Dev Container and CI.
- Some maintenance overhead: we must keep type hints and configuration up-to-date as the code evolves.
- Gradual-typing discipline required: team needs to agree on a baseline strictness level and improve it deliberately to avoid churn.

