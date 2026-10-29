from pathlib import Path

from app.storage.database import connect, transaction


def get_targets(database_path: Path | None = None) -> dict:
    connection = connect(database_path)
    try:
        row = connection.execute("SELECT * FROM daily_targets WHERE id = 1").fetchone()
        if row is None:
            raise RuntimeError("The initialized target row is missing.")
        return dict(row)
    finally:
        connection.close()


def replace_targets(calories: int, protein: int, database_path: Path | None = None) -> dict:
    with transaction(database_path) as connection:
        connection.execute(
            """INSERT INTO daily_targets (id, calorie_target_hundredths, protein_target_hundredths)
               VALUES (1, ?, ?)
               ON CONFLICT(id) DO UPDATE SET
                 calorie_target_hundredths = excluded.calorie_target_hundredths,
                 protein_target_hundredths = excluded.protein_target_hundredths""",
            (calories, protein),
        )
        row = connection.execute("SELECT * FROM daily_targets WHERE id = 1").fetchone()
        return dict(row)