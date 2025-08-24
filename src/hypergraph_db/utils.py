try:
    import pysqlite3 as sqlite3
except ModuleNotFoundError:  # pragma: no cover - fallback when extension not available
    import sqlite3
from pathlib import Path


def load_extensions(conn: sqlite3.Connection):
    """Loads necessary SQLite extensions."""
    conn.enable_load_extension(True)

    # Paths to the compiled extensions
    current_dir = Path(__file__).parent
    sql_dir = current_dir / "sql"

    sqlite_vec_path = sql_dir / "vec0"
    sqlite_lembed_path = sql_dir / "lembed0"

    # Load sqlite-vec extension
    conn.load_extension(str(sqlite_vec_path))

    # Load sqlite-lembed extension
    conn.load_extension(str(sqlite_lembed_path))

    conn.enable_load_extension(False)

    # Register embedding models
    register_embedding_models(conn)


def register_embedding_models(conn: sqlite3.Connection):
    """Registers embedding models for sqlite-lembed."""
    # Path to the embedding model
    current_dir = Path(__file__).parent
    models_dir = current_dir / "sql" / "models"
    model_path = models_dir / "all-MiniLM-L6-v2.e4ce9877.q8_0.gguf"

    # Register the model
    conn.execute(
        """
        INSERT OR IGNORE INTO temp.lembed_models(name, model)
        SELECT ?, lembed_model_from_file(?)
    """,
        ("all-MiniLM-L6-v2", str(model_path)),
    )


def dict_factory(cursor, row):
    """Converts SQLite row to dictionary."""
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}
