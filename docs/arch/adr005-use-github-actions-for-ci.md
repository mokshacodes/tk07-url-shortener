# ADR005: Use GitHub Actions for CI

## Context

We need a continuous integration (CI) system that validates code on every
change with the same tooling we have standardized on: `uv` for dependencies
(ADR01), `pytest` for tests (ADR002), `pyright` for type checking (ADR003),
and `ruff` for linting/formatting (ADR004). The CI system should be easy to
maintain, integrate well with GitHub pull requests, and be fast enough for
frequent feedback.

The CI system should:

- Run on pull requests and main branch updates.
- Support a Linux-based environment aligned with our Dev Container (ADR00).
- Provide clear, inline feedback in GitHub PRs.
- Be simple to configure and maintain for a small team.
- Scale from a minimal pipeline today to richer workflows later.

## Decision

Adopt GitHub Actions as the CI platform for this repository.

Rationale:

- Native integration with GitHub simplifies PR checks, status reporting, and
	developer workflow with no additional credentials or third-party accounts.
- A large library of maintained actions (e.g., checkout, Python setup, cache)
	reduces bespoke scripting and maintenance burden.
- Supports Linux runners consistent with our Dev Container baseline, reducing
	environmental drift.
- Declarative YAML workflows keep configuration in-repo and easy to review.
- Straightforward to extend with caching, test matrices, and artifacts as the
	project grows.

## Considered Options

- GitHub Actions:
	- Pros: native GitHub integration, low friction, rich marketplace, fast
		onboarding, easy to version workflows in-repo.
	- Cons: YAML workflow complexity can grow; hosted runners have usage limits
		(not a concern for this small project).

- GitLab CI:
	- Pros: strong CI features and runners; good UX.
	- Cons: not native to GitHub; requires mirroring or migrating the repo.

- CircleCI:
	- Pros: powerful workflows and caching; good ecosystem.
	- Cons: external service and configuration; adds operational overhead.

- Jenkins (self-hosted):
	- Pros: highly flexible and extensible.
	- Cons: heavy maintenance burden; infrastructure costs and management not
		justified for this project.

## Consequences

- CI runs will be defined in `.github/workflows/` and execute on GitHub-hosted
	Linux runners.
- Developers get immediate, in-context feedback in PRs for tests, linting, and
	type checking.
- Workflow configuration becomes part of the codebase and should be reviewed
	like other changes.
- We must keep workflows aligned with our toolchain versions managed by `uv`.
