from pathlib import Path

from app.storage.database import connect, transaction


def get_meal(meal_id: int, database_path: Path | None = None) -> dict | None:
    connection = connect(database_path)
    try:
        row = connection.execute(
            "SELECT * FROM meal_entries WHERE id = ?", (meal_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        connection.close()


def list_meals(entry_date: str, database_path: Path | None = None) -> list[dict]:
    connection = connect(database_path)
    try:
        rows = connection.execute(
            "SELECT * FROM meal_entries WHERE entry_date = ? ORDER BY id", (entry_date,)
        ).fetchall()
        return [dict(row) for row in rows]
    finally:
        connection.close()


def create_meal(values: dict, database_path: Path | None = None) -> dict:
    with transaction(database_path) as connection:
        cursor = connection.execute(
            """INSERT INTO meal_entries
               (name, category, entry_date, quantity_hundredths,
                calories_per_serving_hundredths, protein_per_serving_hundredths)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                values["name"],
                values["category"],
                values["entry_date"],
                values["quantity_hundredths"],
                values["calories_per_serving_hundredths"],
                values["protein_per_serving_hundredths"],
            ),
        )
        meal_id = cursor.lastrowid
    meal = get_meal(meal_id, database_path)
    if meal is None:
        raise RuntimeError("Committed meal could not be reloaded.")
    return meal


def replace_meal(meal_id: int, values: dict, database_path: Path | None = None) -> dict | None:
    with transaction(database_path) as connection:
        cursor = connection.execute(
            """UPDATE meal_entries SET
               name = ?, category = ?, entry_date = ?, quantity_hundredths = ?,
               calories_per_serving_hundredths = ?, protein_per_serving_hundredths = ?
               WHERE id = ?""",
            (
                values["name"],
                values["category"],
                values["entry_date"],
                values["quantity_hundredths"],
                values["calories_per_serving_hundredths"],
                values["protein_per_serving_hundredths"],
                meal_id,
            ),
        )
        if cursor.rowcount == 0:
            return None
        row = connection.execute("SELECT * FROM meal_entries WHERE id = ?", (meal_id,)).fetchone()
        return dict(row) if row else None


def delete_meal(meal_id: int, database_path: Path | None = None) -> bool:
    with transaction(database_path) as connection:
        cursor = connection.execute("DELETE FROM meal_entries WHERE id = ?", (meal_id,))
        return cursor.rowcount > 0