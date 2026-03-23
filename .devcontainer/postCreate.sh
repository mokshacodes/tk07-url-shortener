#!/usr/bin/env bash
set -euo pipefail

# Dev container post-create hook
# Goal: ensure `uv` is available and dependencies are synced into a project-local `.venv`.

# 1) Ensure `uv` is installed.
# We intentionally use Astral's installer script because `uv` is a standalone Rust binary.
# Installing via `pip` is not recommended here (PyPI naming conflicts + not the canonical install path).
if ! command -v uv >/dev/null 2>&1; then
  curl -LsSf https://astral.sh/uv/install.sh | sh
fi

# 2) Ensure the installed location is on PATH for this script invocation.
export PATH="$HOME/.local/bin:$PATH"

# 3) Create a virtual environment
uv venv --clear

# 4) Sync dependencies from the checked-in lockfile.
# `--frozen` ensures the lockfile is respected (deterministic installs).
# `--group dev` installs our dev tools (pytest, pyright, etc.) into the same project-local `.venv`.
uv sync --frozen --all-groups


