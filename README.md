# metaOA

Meta OA practice: a time-based key-value store with TTL and versioning, built with Python, UV, and pytest. You’ll implement the `Solution` class in `src/database.py` to satisfy a comprehensive unit test suite.

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
```bash
# run entire suite
uv run pytest -q

# run a single test by name
uv run pytest tests/test_database.py::test_set_and_get_immediately -v

# run tests matching a pattern
uv run pytest -k "ttl" -v

# stop at first failure (useful for TDD)
uv run pytest -x
```

## Project layout
```
metaOA/
  pyproject.toml
  pytest.ini
  src/
    database.py          # implement Solution here
  tests/
    test_database.py     # comprehensive unit tests
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
- Start with the first test and iterate:
  - `uv run pytest tests/test_database.py::test_set_and_get_immediately -v`
- Once passing, proceed test-by-test or use `-x` to stop at first failure.
- If imports act oddly, ensure files are saved and clear caches:
  - `rm -rf .pytest_cache src/__pycache__ tests/__pycache__`

