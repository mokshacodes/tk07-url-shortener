# ADR01: Use `uv` for Dependency Management

## Context

The greenfield app we plan to ship in 2026 needs deterministic dependency locking, integrated virtual environment management, and fast installs so agentic AI tools and CI pipelines can iterate quickly. We do not expect to publish the package to PyPI, so we can optimize for developer experience rather than distribution tooling.

## Decision

Adopt `uv` for dependency and environment management. Its Rust-based resolver produces lock files quickly, manages per-project virtual environments, and mirrors familiar `pip`/`poetry` style commands, making it a low-friction choice.

## Considered Options

- `Poetry` offers a rich workflow, but slower resolution and a publication-focused feature set add complexity we do not need.
- Plain `pip` plus `venv` keeps tooling minimal, yet lacks deterministic subdependency locking without extra layers like `pip-tools`.

## Consequences

- New developers must install and learn `uv`, yet command parity with `pip`/`poetry` keeps the learning curve shallow.
- Fast, repeatable installs improve feedback loops for local development, AI agents, and CI runs.