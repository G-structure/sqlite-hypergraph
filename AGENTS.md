# Agent Guidelines

To work with this project, set up the environment and dependencies as follows.

## Environment Setup

1. **Install `just`** (command runner used for setup):
   ```bash
   apt-get update && apt-get install -y just
   ```

2. **Install project dependencies** (includes `pysqlite3-binary` for extension support):
   ```bash
   pip install -e .[dev]
   ```

## Download Required Assets

Use the provided justfile recipes to obtain the embedding model and SQLite extensions:

```bash
just play
```
This will
- download the `all-MiniLM-L6-v2` embedding model,
- install the `sqlite-lembed` extension, and
- install the `sqlite-vec` extension
into `src/hypergraph_db/sql/`.

## Running Tests

Execute the test suite with the project sources on the Python path:

```bash
PYTHONPATH=src pytest
```

## Notes
- The database utilities rely on `pysqlite3` so that `enable_load_extension` is available.
- All setup steps must be run from the repository root.
