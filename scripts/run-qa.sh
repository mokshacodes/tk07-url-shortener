#!/usr/bin/env bash
set -euo pipefail

# QA Script - Runs quality assurance checks in sequence
# Fails at the first step that fails

echo "=========================================="
echo "Starting QA Checks"
echo "=========================================="
echo ""

# Step 1: Format code
echo "----------------------------------------"
echo "Step 1/6: Running ruff format..."
echo "----------------------------------------"
uv run ruff format .
echo "✓ Formatting complete"
echo ""

# Step 2: Fix linting issues automatically
echo "----------------------------------------"
echo "Step 2/6: Running ruff check --fix..."
echo "----------------------------------------"
uv run ruff check --fix .
echo "✓ Auto-fix complete"
echo ""

# Step 3: Check for remaining linting issues
echo "----------------------------------------"
echo "Step 3/6: Running ruff check..."
echo "----------------------------------------"
uv run ruff check .
echo "✓ Linting checks passed"
echo ""

# Step 4: Run type checking on src
echo "----------------------------------------"
echo "Step 4/6: Running pyright..."
echo "----------------------------------------"
uv run pyright --project pyproject.toml 
echo "✓ Type checking passed"
echo ""

# Step 5: Run unit tests only
echo "----------------------------------------"
echo "Step 5/6: Running unit tests..."
echo "----------------------------------------"
uv run pytest
echo "✓ Unit tests passed"
echo ""

# Step 6: Run all tests with coverage report
echo "----------------------------------------"
echo "Step 6/6: Running all tests with coverage..."
echo "----------------------------------------"
uv run pytest --integration --cov=src --cov-report=term-missing
echo "✓ All tests passed with coverage"
echo ""

echo "=========================================="
echo "All QA Checks Passed! ✓"
echo "=========================================="
