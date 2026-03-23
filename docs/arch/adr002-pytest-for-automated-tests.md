# ADR002: Use `pytest` for Automated Testing

## Context

We are building an app that needs to mitigate regressions with automated testing. It should have the ability to support common testing needs (fixtures, mocks) and not only unit tests, but integration and behavioral tests, as well. It needs to be able to report on code coverage.

This repository is intentionally optimized for developer feedback loops (see ADR01 adopting `uv`) and a consistent environment (see ADR00 adopting a Dev Container). The testing tool we choose should:

- Run quickly and give high-signal failure output.
- Scale from "a few unit tests" to integration tests without switching frameworks.
- Have strong ecosystem support for plugins we will likely need (coverage, parallelism, xfail/skip markers, CI-friendly reporting).
- Avoid forcing heavyweight frameworks or bespoke harnesses.

## Decision

Adopt `pytest` as the primary test runner and test framework.

Rationale:

- `pytest` provides concise test authoring (plain `assert`), good failure diffs, and easy test selection (`-k`, `-m`, `-x`, `--lf`) which improves iteration speed.
- Its fixture system supports unit, integration, and behavioral-style tests without introducing a separate framework. Fixtures make dependency setup explicit and reusable across tests.
- The plugin ecosystem is mature and widely used. In particular, coverage reporting via `coverage.py` (typically through `pytest-cov`) is a common, well-supported path.
- `pytest` integrates well with CI systems and IDEs and has a long track record across the Python ecosystem, reducing adoption risk.

Project conventions implied by this decision:

- Tests live under a top-level `tests/` directory.
- Test files are named `test_*.py` (or `*_test.py`) and use plain `assert`.
- Coverage is measured using `coverage.py` (often surfaced through `pytest` plugins) and reported in CI.

## Considered Options

- Standard library `unittest`:
	- Pros: zero additional dependency; familiar to many Python developers.
	- Cons: more boilerplate (classes, assertion methods), weaker ergonomics for parametrization/fixtures, and less pleasant failure output. We would likely end up re-creating patterns `pytest` already solves.

- `nose2`:
	- Pros: inherits some of the "discover tests and run them" convenience from the historical `nose` ecosystem.
	- Cons: smaller ecosystem and mindshare than `pytest`. For a greenfield project, choosing the dominant tool reduces long-term maintenance risk.

- BDD frameworks (e.g., `behave`, `robotframework`):
	- Pros: readable, stakeholder-friendly scenarios.
	- Cons: extra domain-specific tooling and structure before we have evidence that Gherkin-style workflows are needed. If we later want BDD-style tests, `pytest` can still support that style via plugins or patterns without committing the whole suite to a separate runner.

## Consequences

- Improved developer experience: faster iteration and more actionable failure output compared to more boilerplate-heavy frameworks.
- Extensibility: we can adopt common capabilities (coverage, parallel execution, richer reports) via well-supported plugins instead of bespoke scripting.
- Some "magic"/convention: `pytest`’s fixture injection and discovery rules require team discipline (clear fixture naming, avoiding overly broad fixtures) to keep tests readable.
- Dependency footprint: `pytest` (and optional plugins) become part of the project toolchain; we must keep versions compatible with the project’s Python version and CI environment.