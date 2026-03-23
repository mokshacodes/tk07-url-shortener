# ADR00: Standardize Python DevContainer

## Context

This project needs a predictable and reproducible development
environment.

Team members have machines capable of running Docker containers, and
we want a development setup that can also be used in hosted or
cloud-based development environments.

Several forces are in tension:

- We want onboarding to be fast and reliable for new contributors.
- We want local development to match CI closely to reduce
  environment-specific failures.
- We want to minimize maintenance work for the team over time.

## Decision

We will use VS Code Dev Containers with a standard,
Microsoft-maintained Python base image.

We will keep the DevContainer definition lightweight by preferring
configuration over customization and only add project-specific tooling
when it is necessary.

We will use a standard Python .gitignore so temporary files, build
artifacts, local environments, and secrets are not committed.

## Considered Options

- We could run directly on the host OS using a `venv` (or similar).
  This reduces container overhead but increases variability across
  developer machines.
- We could build and maintain a custom Docker image. This gives more
  control but increases the maintenance burden.

## Consequences

- New contributors can start development by opening the repository in
  he container, which reduces setup steps and configuration drift.
- Development and CI are more likely to use the same tooling
  versions, which can reduce “works on my machine” failures.
- The project depends on Docker and VS Code Dev Containers, which may
  add friction for developers who cannot or prefer not to run
  containers.
- Running in a container can reduce performance compared to running
  irectly on the host OS, especially for file-heavy workflows.
- Using an off-the-shelf base image reduces ongoing maintenance but
  limits customization to what the base image supports.