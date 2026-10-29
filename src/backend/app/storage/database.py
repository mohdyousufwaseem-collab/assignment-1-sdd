import sqlite3
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

from app.config import get_database_path


def connect(database_path: Path | None = None) -> sqlite3.Connection:
    path = database_path or get_database_path()
    connection = sqlite3.connect(path, timeout=5.0)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def initialize_database(database_path: Path | None = None) -> Path:
    path = database_path or get_database_path()
    path.parent.mkdir(parents=True, exist_ok=True)
    schema_path = Path(__file__).with_name("schema.sql")
    connection = sqlite3.connect(path, timeout=5.0)
    try:
        connection.executescript(schema_path.read_text(encoding="utf-8"))
        connection.execute(
            """INSERT OR IGNORE INTO daily_targets
               (id, calorie_target_hundredths, protein_target_hundredths)
               VALUES (1, 200000, 5000)"""
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
    return path


@contextmanager
def transaction(database_path: Path | None = None) -> Iterator[sqlite3.Connection]:
    connection = connect(database_path)
    try:
        connection.execute("BEGIN IMMEDIATE")
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()