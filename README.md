# meta OA practice

This project is designed to prepare candidates for the Meta OA Assessment. 

In this project, you will build a time-based key-value store with TTL and versioning, built with Python, UV, and pytest. You’ll implement the `Solution` class in `src/database.py` to satisfy a comprehensive unit test suite.

Inspired by: https://www.hellointerview.com/guides/meta/e5

## Prereqs
- Python 3.11
- uv (https://docs.astral.sh/uv/)

## Setup
```bash
uv python install 3.11          # if you don't have 3.11 managed by uv yet
uv venv --python 3.11           # create .venv
uv sync                         # install dependencies from pyproject.toml
```

## Run tests

Tests are organized into 5 files by category for focused practice:

```bash
# Run all tests (37 total)
uv run pytest tests/ -v

# Run entire suite (quiet mode)
uv run pytest -q

# Run one test file at a time
uv run pytest tests/test_basic.py -v       # 5 tests - basic set/get
uv run pytest tests/test_ttl.py -v         # 8 tests - TTL expiration
uv run pytest tests/test_versioning.py -v  # 10 tests - point-in-time queries
uv run pytest tests/test_delete.py -v      # 6 tests - delete operations
uv run pytest tests/test_advanced.py -v    # 8 tests - edge cases

# Run multiple specific files
uv run pytest tests/test_basic.py tests/test_ttl.py -v

# Run a single test by name
uv run pytest tests/test_basic.py::test_set_and_get_immediately -v

# Run tests matching a pattern (across all files)
uv run pytest -k "ttl" -v

# Stop at first failure (useful for TDD)
uv run pytest -x
```

## Project layout
```
metaOA/
  pyproject.toml
  pytest.ini
  src/
    database.py             # implement Solution here
  tests/
    test_basic.py           # basic set/get operations
    test_ttl.py             # TTL expiration logic
    test_versioning.py      # point-in-time queries
    test_delete.py          # delete operations
    test_advanced.py        # edge cases & boundaries
```

## Problem overview
Implement a time-aware key-value store that supports:
- **set(key, value, timestamp, ttl=None)**: store a value at time with optional TTL
- **get(key, timestamp)**: get the value at a time considering TTL/overwrites
- **get_at(key, timestamp)**: point-in-time retrieval (versioning/time-travel)
- **delete(key, timestamp)**: delete a key at a time

Focus areas include overwrites, expirations, mixed TTL/no-TTL keys, and timeline integrity.

## API reference: `Solution` (to implement in `src/database.py`)
- **set(key: str, value: str, timestamp: int, ttl: int | None = None) -> None**
  - Stores a version for `key` at `timestamp`. If `ttl` is provided, value is valid in `[timestamp, timestamp + ttl)`. A later `set` overwrites for subsequent timestamps.
- **get(key: str, timestamp: int) -> str | None**
  - Returns the effective value of `key` at `timestamp` (latest non-expired set not after `timestamp`).
- **get_at(key: str, timestamp: int) -> str | None**
  - Returns the exact value as it was at `timestamp` (respecting TTL and overwrites).
- **delete(key: str, timestamp: int) -> None**
  - Removes the key from `timestamp` onward until re-set.

## Development workflow
- Start with basic tests and work through each category:
  - `uv run pytest tests/test_basic.py -v`
  - `uv run pytest tests/test_ttl.py -v`
  - `uv run pytest tests/test_versioning.py -v`
  - `uv run pytest tests/test_delete.py -v`
  - `uv run pytest tests/test_advanced.py -v`
- Or use `-x` to stop at first failure across all tests:
  - `uv run pytest tests/ -x`
- If imports act oddly, ensure files are saved and clear caches:
  - `rm -rf .pytest_cache src/__pycache__ tests/__pycache__`

