# ADR007: Tag Integration Tests with Pytest Markers

## Context

We need integration tests to be runnable independently from unit tests, and vice versa. Our test harness is `pytest` (see [ADR002](./adr002-pytest-for-automated-tests.md)). We need an idiomatic, low-friction way to distinguish integration tests for local development and CI.

## Decision

Use `pytest` markers to tag integration tests.

Specifically, mark integration tests with `@pytest.mark.integration` and select them with `-m integration`. Exclude them from unit-only runs with `-m "not integration"`.

## Considered Options

- Directory-based separation (e.g., `tests/integration/`):
	- Pros: clear structure, easy to understand.
	- Cons: brittle when tests span unit/integration behavior; requires strict file placement and can complicate shared fixtures.

- File or test name conventions (e.g., `test_*_integration.py` or `test_*_it.py`):
	- Pros: simple, no extra config.
	- Cons: relies on naming discipline; weaker than explicit intent on the test itself.

- Separate runners or environments (e.g., different `pytest` invocations or `tox` envs only):
	- Pros: strong isolation in CI.
	- Cons: still needs a selector mechanism inside `pytest`; higher maintenance overhead.

## Consequences

- Clear, explicit intent on each test via a marker.
- Simple selection/exclusion via `-m` for local workflows and CI.
- Requires registering the `integration` marker in `pytest` config to avoid warnings.
- Teams must apply the marker consistently for accurate suite composition.