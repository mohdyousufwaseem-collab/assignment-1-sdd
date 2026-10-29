PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS meal_entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL CHECK (length(trim(name)) BETWEEN 1 AND 80),
    category TEXT NOT NULL CHECK (category IN ('Breakfast', 'Lunch', 'Dinner', 'Snack')),
    entry_date TEXT NOT NULL CHECK (
        entry_date GLOB '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9]'
    ),
    quantity_hundredths INTEGER NOT NULL CHECK (quantity_hundredths BETWEEN 1 AND 10000),
    calories_per_serving_hundredths INTEGER NOT NULL CHECK (
        calories_per_serving_hundredths BETWEEN 0 AND 1000000
    ),
    protein_per_serving_hundredths INTEGER NOT NULL CHECK (
        protein_per_serving_hundredths BETWEEN 0 AND 100000
    )
);

CREATE INDEX IF NOT EXISTS idx_meal_entries_date ON meal_entries(entry_date);

CREATE TABLE IF NOT EXISTS daily_targets (
    id INTEGER PRIMARY KEY CHECK (id = 1),
    calorie_target_hundredths INTEGER NOT NULL CHECK (
        calorie_target_hundredths BETWEEN 100 AND 10000000
    ),
    protein_target_hundredths INTEGER NOT NULL CHECK (
        protein_target_hundredths BETWEEN 1 AND 1000000
    )
);